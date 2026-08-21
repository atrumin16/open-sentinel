# -*- coding: utf-8 -*-
"""
OpenSentinel Unified Notification Dispatcher
Coordinates multi-channel alerts (Discord, Telegram, WhatsApp) with anti-spam session lock.
"""

import datetime
import json
import psutil
from ..config import load_config, BOOT_SESSION_FILE
from ..core.hardware import get_full_hardware_summary
from ..core.network import get_network_summary
from .discord import DiscordNotifier
from .telegram import TelegramNotifier
from .whatsapp import WhatsAppNotifier

def get_active_notifiers(config: dict) -> list:
    """Instancia todos los proveedores de notificación disponibles."""
    return [
        DiscordNotifier(config),
        TelegramNotifier(config),
        WhatsAppNotifier(config)
    ]

def dispatch_boot_alert(force=False) -> dict:
    """Envía la alerta de inicio a todos los canales habilitados evitando spam."""
    cfg = load_config()
    current_boot_ts = int(psutil.boot_time())

    # Comprobación de Anti-Spam por sesión de arranque
    if not force and BOOT_SESSION_FILE.exists():
        try:
            with open(BOOT_SESSION_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
                if state.get("last_alerted_boot_time") == current_boot_ts:
                    return {
                        "sent": False,
                        "reason": "anti_spam_blocked",
                        "msg": "Alerta de inicio ya enviada previamente para esta sesion de Windows."
                    }
        except Exception:
            pass

    hw = get_full_hardware_summary()
    net = get_network_summary(port=cfg.get("PORT", 8888))
    notifiers = get_active_notifiers(cfg)

    results = {}
    any_success = False

    for n in notifiers:
        if n.is_enabled():
            ok = n.send_boot_alert(hw, net)
            results[n.name] = ok
            if ok:
                any_success = True

    if any_success or not any(n.is_enabled() for n in notifiers):
        # Guardar sesión de arranque
        try:
            with open(BOOT_SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "last_alerted_boot_time": current_boot_ts,
                    "last_alert_sent_at": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "hostname": hw["hostname"]
                }, f, indent=2)
        except Exception:
            pass

    return {
        "sent": any_success,
        "results": results,
        "msg": "Alertas transmitidas a los canales activos" if any_success else "Ningun canal activo o fallo en el envio"
    }

def dispatch_evidence_alert(img_bytes: bytes, title="EVIDENCIA DE SEGURIDAD", reason="Auditoria Solicitada") -> dict:
    """Transmite una foto de evidencia forense a todos los canales habilitados."""
    cfg = load_config()
    notifiers = get_active_notifiers(cfg)
    results = {}

    for n in notifiers:
        if n.is_enabled():
            results[n.name] = n.send_evidence_alert(img_bytes, title, reason)

    return {"results": results}

def send_test_notification(channel: str, custom_config: dict = None) -> dict:
    """Envía un mensaje de prueba a un canal específico para validar credenciales."""
    cfg = custom_config or load_config()
    channel = channel.lower()

    if channel == "discord":
        return DiscordNotifier(cfg).send_test_message()
    elif channel == "telegram":
        return TelegramNotifier(cfg).send_test_message()
    elif channel == "whatsapp":
        return WhatsAppNotifier(cfg).send_test_message()
    else:
        return {"success": False, "msg": f"Canal desconocido: {channel}"}
