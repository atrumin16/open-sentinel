# -*- coding: utf-8 -*-
"""
OpenSentinel Web Application & REST API Server
Flask-based hardened dashboard with dynamic telemetry, media streaming, and config endpoints.
"""

import io
import json
import os
import socket
import threading
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, abort, send_from_directory
import psutil

from ..config import load_config, save_config, CLIPS_DIR
from ..core.hardware import get_full_hardware_summary, get_active_window_title
from ..core.network import get_network_summary, is_trusted_ip, send_wol_packet
from ..core.surveillance import (
    get_live_screen_image, get_shared_webcam_frame, generate_locked_screen_placeholder,
    export_in_ram_video, IS_OPTIMIZED_MODE, CURRENT_WORKLOAD_NAME
)
from ..core.defcon import trigger_defcon_panic, get_last_defcon_evidence, get_defcon_placeholder_bytes
from ..core.power import (
    lock_workstation, sleep_system, schedule_shutdown, schedule_reboot,
    cancel_power_action, wake_screen, toggle_mute, set_volume_level, show_screen_alert
)
from ..core.process_mgr import get_top_processes, kill_process_by_pid
from ..notifiers.dispatcher import dispatch_boot_alert, dispatch_evidence_alert, send_test_notification
from ..i18n import t, get_web_translations, SUPPORTED_LANGUAGES, WEB_TRANSLATIONS

def is_trusted_ip(ip: str) -> bool:
    if not ip: return False
    return ip.startswith("100.") or ip.startswith("192.168.") or ip.startswith("10.") or ip.startswith("172.") or ip in ("127.0.0.1", "::1")

SINGLE_INSTANCE_SOCKET = None
def check_single_instance(port: int) -> bool:
    global SINGLE_INSTANCE_SOCKET
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", port + 100))
        s.listen(1)
        SINGLE_INSTANCE_SOCKET = s
        return True
    except socket.error:
        return False

def create_app():
    templates_dir = Path(__file__).parent / "templates"
    static_dir = Path(__file__).parent / "static"
    app = Flask(__name__, template_folder=str(templates_dir), static_folder=str(static_dir))
    app.secret_key = os.urandom(32)

    @app.before_request
    def security_gate():
        if not is_trusted_ip(request.remote_addr):
            abort(403)

    # --------------------------------------------------------------------------
    # VISTAS PRINCIPALES
    # --------------------------------------------------------------------------
    @app.route("/")
    def index():
        cfg = load_config()
        hw = get_full_hardware_summary()
        net = get_network_summary(port=cfg.get("PORT", 8888))
        lang = cfg.get("LANGUAGE", "en")
        translations = get_web_translations(lang)
        return render_template(
            "index.html",
            config=cfg,
            hw=hw,
            net=net,
            lang=lang,
            translations=translations,
            all_translations=WEB_TRANSLATIONS,
            supported_languages=SUPPORTED_LANGUAGES
        )

    @app.route("/api/i18n")
    def api_i18n():
        target_lang = request.args.get("lang")
        if target_lang:
            return jsonify(get_web_translations(target_lang))
        return jsonify({
            "supported": SUPPORTED_LANGUAGES,
            "translations": WEB_TRANSLATIONS
        })

    # --------------------------------------------------------------------------
    # API: TELEMETRÍA Y PROCESOS
    # --------------------------------------------------------------------------
    @app.route("/api/stats")
    def api_stats():
        hw = get_full_hardware_summary()
        return jsonify({
            "cpu_pct": psutil.cpu_percent(interval=None),
            "ram": hw["ram"],
            "disks": hw["disks"],
            "uptime": hw["uptime"],
            "active_window": get_active_window_title(),
            "is_optimized": IS_OPTIMIZED_MODE,
            "workload_name": CURRENT_WORKLOAD_NAME or ""
        })

    @app.route("/api/processes")
    def api_processes():
        return jsonify(get_top_processes(limit=30))

    @app.route("/api/processes/kill", methods=["POST"])
    def api_kill_proc():
        pid = request.args.get("pid", type=int)
        if not pid:
            return jsonify({"success": False, "msg": "PID no especificado"}), 400
        res = kill_process_by_pid(pid)
        return jsonify(res), 200 if res["success"] else 400

    # --------------------------------------------------------------------------
    # API: VIGILANCIA & MEDIOS FORENSES
    # --------------------------------------------------------------------------
    @app.route("/api/screenshot")
    def api_screenshot():
        img = get_live_screen_image()
        buf = io.BytesIO()
        if img is not None:
            img.save(buf, format="JPEG", quality=80)
        else:
            generate_locked_screen_placeholder().save(buf, format="JPEG", quality=85)
        buf.seek(0)
        return send_file(buf, mimetype="image/jpeg")

    @app.route("/api/webcam")
    def api_webcam():
        frame = get_shared_webcam_frame()
        if frame is not None:
            import cv2
            _, b = cv2.imencode(".jpg", frame)
            return send_file(io.BytesIO(b.tobytes()), mimetype="image/jpeg")
        
        buf = io.BytesIO()
        from PIL import Image, ImageDraw
        img = Image.new("RGB", (640, 360), color=(10, 14, 23))
        d = ImageDraw.Draw(img)
        d.text((200, 160), "SENSOR OPTICO NO DISPONIBLE", fill=(148, 163, 184))
        img.save(buf, format="JPEG")
        buf.seek(0)
        return send_file(buf, mimetype="image/jpeg")

    @app.route("/api/generate_clip", methods=["POST"])
    def api_generate_clip():
        res = export_in_ram_video(CLIPS_DIR)
        return jsonify(res), 200 if "url" in res else 400

    @app.route("/api/clear_temp_clip", methods=["POST"])
    def api_clear_clip():
        for f in CLIPS_DIR.glob("*.mp4"):
            try: f.unlink()
            except Exception: pass
        return jsonify({"msg": "Clip temporal liberado"})

    @app.route("/clips/<path:filename>")
    def serve_clip(filename):
        return send_from_directory(CLIPS_DIR, filename)

    # --------------------------------------------------------------------------
    # API: SEGURIDAD & PROTOCOLO DEFCON-1
    # --------------------------------------------------------------------------
    @app.route("/api/defcon/panic", methods=["POST"])
    def api_defcon_panic():
        res = trigger_defcon_panic()
        # Disparar alerta fotográfica silenciosa a todos los canales
        if res.get("photo_bytes"):
            threading.Thread(target=dispatch_evidence_alert, args=(res["photo_bytes"], "🚨 DEFCON-1 MODO PÁNICO", "Bloqueo inmediato y registro de intruso")).start()
        return jsonify(res)

    @app.route("/api/last_defcon_photo")
    def api_last_defcon():
        photo, _ = get_last_defcon_evidence()
        if photo:
            return send_file(io.BytesIO(photo), mimetype="image/jpeg")
        return send_file(get_defcon_placeholder_bytes(), mimetype="image/jpeg")

    # --------------------------------------------------------------------------
    # API: GESTIÓN DE ENERGÍA Y CONTROL
    # --------------------------------------------------------------------------
    @app.route("/api/power/lock", methods=["POST"])
    def api_lock():
        lock_workstation()
        return jsonify({"msg": "Sesion bloqueada"})

    @app.route("/api/power/sleep", methods=["POST"])
    def api_sleep():
        sleep_system()
        return jsonify({"msg": "Estacion suspendida"})

    @app.route("/api/power/shutdown", methods=["POST"])
    def api_shutdown():
        schedule_shutdown(10)
        return jsonify({"msg": "Apagado programado en 10s"})

    @app.route("/api/power/reboot", methods=["POST"])
    def api_reboot():
        schedule_reboot(10)
        return jsonify({"msg": "Reinicio programado en 10s"})

    @app.route("/api/power/cancel", methods=["POST"])
    def api_cancel():
        res = cancel_power_action()
        return jsonify({"msg": "Operacion anulada con exito" if res else "Sin operaciones pendientes"})

    @app.route("/api/power/wake_screen", methods=["POST"])
    def api_wake_screen():
        wake_screen()
        return jsonify({"msg": "Orden de encendido de pantalla enviada"})

    @app.route("/api/power/wake_pc", methods=["POST"])
    def api_wake_pc():
        res = send_wol_packet()
        return jsonify({"msg": "Paquete WoL emitido" if res else "Error WoL"})

    @app.route("/api/power/mute", methods=["POST"])
    def api_mute():
        toggle_mute()
        return jsonify({"msg": "Audio silenciado/alternado"})

    @app.route("/api/power/volume", methods=["POST"])
    def api_volume():
        level = request.args.get("level", default=50, type=int)
        set_volume_level(level)
        return jsonify({"msg": f"Volumen fijado al {level}%"})

    # --------------------------------------------------------------------------
    # API: NOTIFICACIONES & CONFIGURACIÓN
    # --------------------------------------------------------------------------
    @app.route("/api/send_boot_alert", methods=["POST"])
    def api_send_boot_alert():
        threading.Thread(target=dispatch_boot_alert, kwargs={"force": True}).start()
        return jsonify({"msg": "Informe transmitido a todos los canales activos"})

    @app.route("/api/send_evidence", methods=["POST"])
    def api_send_evidence():
        raw_frame = get_shared_webcam_frame()
        if raw_frame is not None:
            import cv2
            _, b = cv2.imencode(".jpg", raw_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            threading.Thread(target=dispatch_evidence_alert, args=(b.tobytes(), "EVIDENCIA FORENSE", "Captura solicitada desde el panel")).start()
            return jsonify({"msg": "Evidencia transmitida a los canales activos"})
        return jsonify({"msg": "Sensor optico no disponible"}), 400

    @app.route("/api/test_notification", methods=["POST"])
    def api_test_notif():
        channel = request.args.get("channel", "discord")
        res = send_test_notification(channel)
        return jsonify(res)

    @app.route("/api/config", methods=["GET", "POST"])
    def api_manage_config():
        if request.method == "GET":
            return jsonify(load_config())
        
        data = request.get_json() or {}
        cfg = load_config()
        cfg.update(data)
        ok = save_config(cfg)
        current_lang = cfg.get("LANGUAGE", "en")
        msg = t("settings_saved", current_lang) if ok else t("settings_save_error", current_lang)
        return jsonify({"success": ok, "msg": msg})

    return app
