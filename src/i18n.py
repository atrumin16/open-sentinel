# -*- coding: utf-8 -*-
"""
OpenSentinel Internationalization (i18n) Engine
Supports English (en) and Spanish (es) with extensible dictionary architecture.
Provides translations for Notifiers (Discord, Telegram, WhatsApp), Web UI, CLI Wizard, and API.
"""

from typing import Dict, Any

SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Español"
}

DEFAULT_LANGUAGE = "en"

# ---------------------------------------------------------------------------
# TRANSLATION DICTIONARIES
# ---------------------------------------------------------------------------
MESSAGES: Dict[str, Dict[str, str]] = {
    # --- Discord Embeds ---
    "discord_boot_title": {
        "en": "🟢 SYSTEM ONLINE // {hostname}",
        "es": "🟢 SISTEMA EN LÍNEA // {hostname}"
    },
    "discord_boot_desc_header": {
        "en": "**REMOTE CONTROL CENTER AVAILABLE:**",
        "es": "**CENTRO DE CONTROL REMOTO DISPONIBLE:**"
    },
    "discord_remote_active": {
        "en": "• 🚀 **Remote Access (Tailscale P2P):** [Open Remote Dashboard]({url})",
        "es": "• 🚀 **Acceso Remoto (Tailscale P2P):** [Abrir Panel Remoto]({url})"
    },
    "discord_remote_inactive": {
        "en": "• 🚀 **Remote Access (Tailscale P2P):** *Unavailable at boot*",
        "es": "• 🚀 **Acceso Remoto (Tailscale P2P):** *No disponible en el arranque*"
    },
    "discord_local_link": {
        "en": "• 🏠 **Local Access (Home LAN):** [Open Local Dashboard]({url})",
        "es": "• 🏠 **Acceso Local (Red Doméstica LAN):** [Abrir Panel Local]({url})"
    },
    "discord_field_station": {
        "en": "💻 Workstation & User",
        "es": "💻 Estación & Usuario"
    },
    "discord_field_conn_time": {
        "en": "⏱️ Connection Time",
        "es": "⏱️ Hora de Conexión"
    },
    "discord_field_hw": {
        "en": "⚡ Hardware Specs",
        "es": "⚡ Especificaciones de Hardware"
    },
    "discord_field_network": {
        "en": "🌐 Network & Security Link",
        "es": "🌐 Red & Enlace de Seguridad"
    },
    "discord_footer_boot": {
        "en": "{server_name} • Boot Session Verified",
        "es": "{server_name} • Sesión de Inicio Verificada"
    },
    "discord_evidence_content": {
        "en": "### [SENTINEL // FORENSIC AUDIT] {reason}\n> **Time:** `{time}`",
        "es": "### [SENTINEL // AUDITORÍA FORENSE] {reason}\n> **Hora:** `{time}`"
    },
    "discord_evidence_desc": {
        "en": "**Reason:** {reason}\n**Security:** Evidence captured from RAM buffer.",
        "es": "**Motivo:** {reason}\n**Seguridad:** Evidencia capturada desde RAM."
    },
    "discord_evidence_footer": {
        "en": "{server_name} | Forensic Record",
        "es": "{server_name} | Registro Forense"
    },
    "discord_test_msg": {
        "en": "🔔 **[OpenSentinel]** Test message received successfully from control panel.",
        "es": "🔔 **[OpenSentinel]** Mensaje de prueba recibido correctamente desde el panel de control."
    },

    # --- Telegram Alerts ---
    "telegram_boot_text": {
        "en": (
            "🟢 *[OPENSENTINEL]* Node Online\n\n"
            "💻 *Workstation:* `{user} @ {hostname}`\n"
            "⏱️ *Time:* `{time}`\n"
            "⚡ *Hardware:* `{cpu}` | `{gpu}` | `{ram} GB RAM`\n"
            "🌐 *Network:* `{public_ip}` ({isp} - {location})\n\n"
            "🔗 *DASHBOARD ACCESS:*\n"
            "• [Remote Dashboard (Tailscale)]({url_remote})\n"
            "• [Local Dashboard (LAN)]({url_local})"
        ),
        "es": (
            "🟢 *[OPENSENTINEL]* Nodo en Línea\n\n"
            "💻 *Estación:* `{user} @ {hostname}`\n"
            "⏱️ *Hora:* `{time}`\n"
            "⚡ *Hardware:* `{cpu}` | `{gpu}` | `{ram} GB RAM`\n"
            "🌐 *Red:* `{public_ip}` ({isp} - {location})\n\n"
            "🔗 *ACCESO AL PANEL:*\n"
            "• [Panel Remoto (Tailscale)]({url_remote})\n"
            "• [Panel Local (LAN)]({url_local})"
        )
    },
    "telegram_evidence_caption": {
        "en": "🚨 *[{title}]*\n\n📋 *Reason:* {reason}\n⏱️ *Time:* `{time}`\n🛡️ *Status:* Evidence captured from RAM",
        "es": "🚨 *[{title}]*\n\n📋 *Motivo:* {reason}\n⏱️ *Hora:* `{time}`\n🛡️ *Estado:* Evidencia capturada desde RAM"
    },
    "telegram_test_msg": {
        "en": "🔔 *[OpenSentinel]* Test message received successfully in Telegram.",
        "es": "🔔 *[OpenSentinel]* Mensaje de prueba recibido correctamente en Telegram."
    },

    # --- WhatsApp Alerts ---
    "whatsapp_boot_text": {
        "en": (
            "🟢 *[OPENSENTINEL]* Node Online\n"
            "💻 Workstation: {user} @ {hostname}\n"
            "⏱️ Time: {time}\n"
            "⚡ Hardware: {cpu} | {ram} GB RAM\n"
            "🌐 Network: {public_ip} ({isp})\n\n"
            "🔗 Remote Dashboard (Tailscale): {url_remote}\n"
            "🏠 Local Dashboard (LAN): {url_local}"
        ),
        "es": (
            "🟢 *[OPENSENTINEL]* Nodo Online\n"
            "💻 Estacion: {user} @ {hostname}\n"
            "⏱️ Hora: {time}\n"
            "⚡ Hardware: {cpu} | {ram} GB RAM\n"
            "🌐 Red: {public_ip} ({isp})\n\n"
            "🔗 Panel Remoto (Tailscale): {url_remote}\n"
            "🏠 Panel Local (LAN): {url_local}"
        )
    },
    "whatsapp_evidence_text": {
        "en": "🚨 *[OPENSENTINEL - {title}]*\n\nReason: {reason}\nTime: {time}\nEvidence captured and saved in dashboard RAM.",
        "es": "🚨 *[OPENSENTINEL - {title}]*\n\nMotivo: {reason}\nHora: {time}\nEvidencia capturada y guardada en RAM del panel."
    },
    "whatsapp_test_msg": {
        "en": "🔔 *[OpenSentinel]* WhatsApp test message received successfully.",
        "es": "🔔 *[OpenSentinel]* Mensaje de prueba de WhatsApp recibido correctamente."
    },

    # --- Common API & Status Messages ---
    "session_locked": {
        "en": "Session locked",
        "es": "Sesion bloqueada"
    },
    "system_suspended": {
        "en": "Workstation suspended",
        "es": "Estacion suspendida"
    },
    "shutdown_scheduled": {
        "en": "Shutdown scheduled in 10s",
        "es": "Apagado programado en 10s"
    },
    "reboot_scheduled": {
        "en": "Reboot scheduled in 10s",
        "es": "Reinicio programado en 10s"
    },
    "operation_cancelled": {
        "en": "Operation aborted successfully",
        "es": "Operacion anulada con exito"
    },
    "no_pending_ops": {
        "en": "No pending operations",
        "es": "Sin operaciones pendientes"
    },
    "screen_wake_sent": {
        "en": "Display wake command dispatched",
        "es": "Orden de encendido de pantalla enviada"
    },
    "wol_packet_sent": {
        "en": "WoL packet broadcasted",
        "es": "Paquete WoL emitido"
    },
    "wol_error": {
        "en": "WoL dispatch error",
        "es": "Error WoL"
    },
    "audio_muted": {
        "en": "Audio muted / toggled",
        "es": "Audio silenciado/alternado"
    },
    "volume_set": {
        "en": "Volume set to {level}%",
        "es": "Volumen fijado al {level}%"
    },
    "report_dispatched": {
        "en": "Report transmitted to all active channels",
        "es": "Informe transmitido a todos los canales activos"
    },
    "evidence_dispatched": {
        "en": "Evidence transmitted to active channels",
        "es": "Evidencia transmitida a los canales activos"
    },
    "sensor_unavailable": {
        "en": "Optical sensor unavailable",
        "es": "Sensor optico no disponible"
    },
    "settings_saved": {
        "en": "Settings saved successfully",
        "es": "Ajustes guardados correctamente"
    },
    "settings_save_error": {
        "en": "Error saving settings",
        "es": "Error al guardar configuracion"
    },
    "defcon_executed": {
        "en": "DEFCON-1 EXECUTED: Workstation locked and evidence secured",
        "es": "DEFCON-1 EJECUTADO: Estacion bloqueada y evidencia asegurada"
    },
    "defcon_placeholder": {
        "en": "NO PRIOR DEFCON RECORDS",
        "es": "SIN REGISTROS DEFCON PREVIOS"
    },
    "camera_placeholder": {
        "en": "OPTICAL SENSOR UNAVAILABLE",
        "es": "SENSOR OPTICO NO DISPONIBLE"
    },
    "forensic_watermark": {
        "en": "FORENSIC RECORD // {ts}",
        "es": "REGISTRO FORENSE // {ts}"
    },
    "anti_spam_blocked": {
        "en": "Boot alert already dispatched for this physical Windows session.",
        "es": "Alerta de inicio ya enviada previamente para esta sesion de Windows."
    }
}

# ---------------------------------------------------------------------------
# WEB UI TRANSLATIONS (Directly injected to frontend for zero-latency toggle)
# ---------------------------------------------------------------------------
WEB_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "en": {
        "protected_session": "PROTECTED SESSION",
        "status_online": "ONLINE",
        "tab_metrics": "Metrics",
        "tab_surveillance": "Surveillance",
        "tab_security": "Security",
        "tab_processes": "Processes",
        "tab_config": "Settings",

        # Telemetry Tab
        "telemetry_title": "SYSTEM TELEMETRY",
        "uptime": "Uptime",
        "cpu_load": "CPU Load",
        "ram_memory": "RAM Memory",
        "drive": "Drive",
        "free_of": "free",
        "used": "used",
        "btn_broadcast_report": "📡 BROADCAST REPORT TO ALERT CHANNELS",
        "btn_broadcast_report_sub": "Sends telemetry and active links to Discord / Telegram / WhatsApp",
        "hw_specs_title": "HARDWARE SPECIFICATIONS",
        "detected_badge": "DETECTED",
        "processor": "Processor",
        "gpu": "Graphics Card",
        "ram_physical": "Physical Memory",
        "active_window": "Focused Window",
        "gaming_mode": "Gaming/Load Mode",
        "residual_zero": "0% RESIDUAL LOAD",

        # Surveillance Tab
        "surveillance_title": "FORENSIC CENTER & CAPTURE",
        "in_ram_badge": "100% IN RAM",
        "btn_capture_screen": "CAPTURE SCREEN",
        "btn_capture_screen_sub": "Direct GDI hardware",
        "btn_webcam_snap": "WEBCAM SNAPSHOT",
        "btn_webcam_snap_sub": "Live optical sensor",
        "btn_export_video": "EXPORT VIDEO (5 MIN)",
        "btn_export_video_sub": "Screen + PiP Webcam",
        "btn_send_evidence": "SEND EVIDENCE",
        "btn_send_evidence_sub": "Push photo to channels",
        "forensic_evidence_label": "Forensic Evidence",
        "btn_save": "SAVE",
        "btn_close": "CLOSE",
        "intruder_card_title": "🚨 INTRUDER LOG (DEFCON-1)",
        "intruder_logged_badge": "RECORDED",
        "intruder_card_desc": "Silent frame captured in RAM upon triggering panic mode:",

        # Security Tab
        "defcon_title": "DEFCON-1 PROTOCOL // ANTI-INTRUDER",
        "instant_badge": "INSTANT",
        "defcon_desc": "Triggers panic lockdown: captures a <strong>silent intruder photo</strong> in RAM, mutes audio hardware, and <strong>locks Windows in 1 millisecond</strong>.",
        "btn_trigger_defcon": "🚨 ACTIVATE DEFCON-1 LOCKDOWN",
        "btn_trigger_defcon_sub": "Silent Photo + Forced Lock",
        "power_title": "SESSION & POWER MANAGEMENT",
        "remote_control_badge": "REMOTE CONTROL",
        "btn_lock_session": "LOCK SESSION",
        "btn_sleep_mode": "SLEEP MODE",
        "btn_sleep_sub": "S3 Standby",
        "btn_shutdown": "SHUTDOWN SYSTEM",
        "btn_shutdown_sub": "10s Timer",
        "btn_reboot": "REBOOT SYSTEM",
        "btn_reboot_sub": "10s Safe Reboot",
        "display_audio_title": "DISPLAY, AUDIO & ALARMS",
        "btn_wake_screen": "WAKE DISPLAY",
        "btn_wake_screen_sub": "Wake Monitor / DWM",
        "btn_wake_pc": "WAKE PC (WoL)",
        "btn_wake_pc_sub": "Magic Packet Broadcast",
        "btn_mute": "MUTE AUDIO",
        "btn_vol50": "VOL 50%",
        "btn_vol50_sub": "Medium Level",
        "btn_cancel_power": "CANCEL",
        "btn_cancel_power_sub": "Abort Action",

        # Processes Tab
        "processes_title": "ACTIVE PROCESSES (TOP MEMORY)",
        "btn_refresh": "REFRESH",
        "loading_processes": "Loading processes...",
        "no_heavy_processes": "No heavy processes running.",
        "error_listing_processes": "Error listing processes.",
        "btn_kill": "KILL",

        # Settings Tab
        "channels_title": "NOTIFICATION CHANNELS",
        "config_meta": "SETTINGS",
        "lbl_language": "LANGUAGE / IDIOMA",
        "btn_test_discord": "🔔 Test Discord",
        "btn_test_telegram": "🔔 Test Telegram",
        "btn_test_whatsapp": "🔔 Test WhatsApp",
        "btn_save_config": "💾 SAVE SETTINGS",

        # Modals & Alerts
        "modal_title": "SECURITY CONFIRMATION",
        "modal_default_msg": "Do you wish to execute this remote action?",
        "modal_btn_execute": "EXECUTE",
        "modal_btn_cancel": "CANCEL",
        "modal_confirm_shutdown_title": "SHUTDOWN SYSTEM",
        "modal_confirm_shutdown_msg": "Confirm remote system shutdown?",
        "modal_confirm_reboot_title": "REBOOT SYSTEM",
        "modal_confirm_reboot_msg": "Confirm remote system reboot?",
        "modal_confirm_defcon_title": "ACTIVATE DEFCON-1 PANIC MODE",
        "modal_confirm_defcon_msg": "Confirm immediate forced workstation lock and silent evidence capture?",
        "modal_confirm_kill_title": "TERMINATE PROCESS",
        "modal_confirm_kill_msg": "Terminate process {name} (PID: {pid})?",

        # Toasts
        "toast_broadcasting_report": "Transmitting report to channels...",
        "toast_sending_evidence": "Transmitting evidence to channels...",
        "toast_compiling_video": "Compiling forensic video from RAM buffer...",
        "toast_video_ready": "Video ready",
        "toast_video_error": "Error compiling video",
        "toast_defcon_firing": "TRIGGERING DEFCON-1 LOCKDOWN...",
        "toast_defcon_done": "DEFCON-1 EXECUTED",
        "toast_defcon_error": "Error executing DEFCON-1",
        "toast_locking": "Locking session...",
        "toast_sleeping": "Suspending PC...",
        "toast_shutting_down": "Shutting down in 10s...",
        "toast_rebooting": "Rebooting PC in 10s...",
        "toast_waking_screen": "Waking display...",
        "toast_sending_wol": "Sending WoL packet...",
        "toast_toggling_audio": "Toggling audio mute...",
        "toast_setting_volume": "Setting volume to 50%...",
        "toast_cancelling": "Cancelling power action...",
        "toast_killing": "Terminating {name}...",
        "toast_testing_channel": "Sending test to {channel}...",
        "toast_saving_settings": "Saving settings...",
        "toast_settings_saved": "Settings saved successfully",
        "toast_settings_error": "Error saving settings",
        "toast_fetch_media": "Fetching {label}...",
        "toast_comm_error": "Server communication error"
    },

    "es": {
        "protected_session": "SESIÓN PROTEGIDA",
        "status_online": "ONLINE",
        "tab_metrics": "Métricas",
        "tab_surveillance": "Vigilancia",
        "tab_security": "Seguridad",
        "tab_processes": "Procesos",
        "tab_config": "Ajustes",

        # Pestaña Telemetría
        "telemetry_title": "TELEMETRÍA DEL SISTEMA",
        "uptime": "Uptime",
        "cpu_load": "Carga de CPU",
        "ram_memory": "Memoria RAM",
        "drive": "Unidad",
        "free_of": "libres",
        "used": "ocupado",
        "btn_broadcast_report": "📡 TRANSMITIR INFORME A CANALES DE ALERTA",
        "btn_broadcast_report_sub": "Envía telemetría y enlaces activos a Discord / Telegram / WhatsApp",
        "hw_specs_title": "ESPECIFICACIONES DEL HARDWARE",
        "detected_badge": "DETECTADO",
        "processor": "Procesador",
        "gpu": "Tarjeta Gráfica",
        "ram_physical": "Memoria Física",
        "active_window": "Ventana en Foco",
        "gaming_mode": "Modo Juegos/Carga",
        "residual_zero": "0% CARGA RESIDUAL",

        # Pestaña Vigilancia
        "surveillance_title": "CENTRO FORENSE & CAPTURA",
        "in_ram_badge": "100% EN RAM",
        "btn_capture_screen": "CAPTURAR PANTALLA",
        "btn_capture_screen_sub": "Hardware GDI directo",
        "btn_webcam_snap": "FOTO WEBCAM",
        "btn_webcam_snap_sub": "Sensor óptico en vivo",
        "btn_export_video": "EXPORTAR VIDEO (5 MIN)",
        "btn_export_video_sub": "Pantalla + PiP Webcam",
        "btn_send_evidence": "ENVIAR EVIDENCIA",
        "btn_send_evidence_sub": "Guarda foto en canales",
        "forensic_evidence_label": "Evidencia Forense",
        "btn_save": "GUARDAR",
        "btn_close": "CERRAR",
        "intruder_card_title": "🚨 REGISTRO DE INTRUSO (DEFCON-1)",
        "intruder_logged_badge": "REGISTRADO",
        "intruder_card_desc": "Fotograma silencioso asegurado en RAM al disparar el modo pánico:",

        # Pestaña Seguridad
        "defcon_title": "PROTOCOLO DEFCON-1 // ANTI-INTRUSOS",
        "instant_badge": "INSTANTÁNEO",
        "defcon_desc": "Dispara el bloqueo de pánico: toma una <strong>foto silenciosa del intruso</strong> en RAM, silencia el hardware y <strong>bloquea Windows en 1 milisegundo</strong>.",
        "btn_trigger_defcon": "🚨 ACTIVAR BLOQUEO DEFCON 1",
        "btn_trigger_defcon_sub": "Foto Silenciosa + Bloqueo Forzoso",
        "power_title": "GESTIÓN DE SESIÓN Y ENERGÍA",
        "remote_control_badge": "CONTROL REMOTO",
        "btn_lock_session": "BLOQUEAR SESIÓN",
        "btn_sleep_mode": "MODO SUSPENSIÓN",
        "btn_sleep_sub": "Reposo S3",
        "btn_shutdown": "APAGAR SISTEMA",
        "btn_shutdown_sub": "Temporizador 10s",
        "btn_reboot": "REINICIAR SISTEMA",
        "btn_reboot_sub": "Reinicio Seguro 10s",
        "display_audio_title": "PANTALLA, AUDIO Y ALARMAS",
        "btn_wake_screen": "DESPERTAR PANTALLA",
        "btn_wake_screen_sub": "Encender Monitor / DWM",
        "btn_wake_pc": "DESPERTAR PC (WoL)",
        "btn_wake_pc_sub": "Magic Packet Broadcast",
        "btn_mute": "SILENCIAR AUDIO",
        "btn_vol50": "VOL 50%",
        "btn_vol50_sub": "Nivel Medio",
        "btn_cancel_power": "CANCELAR",
        "btn_cancel_power_sub": "Abortar",

        # Pestaña Procesos
        "processes_title": "PROCESOS ACTIVOS (TOP MEMORIA)",
        "btn_refresh": "REFRESCAR",
        "loading_processes": "Cargando procesos...",
        "no_heavy_processes": "Sin procesos pesados en ejecución.",
        "error_listing_processes": "Error al listar procesos.",
        "btn_kill": "CERRAR",

        # Pestaña Ajustes
        "channels_title": "CANALES DE NOTIFICACIÓN",
        "config_meta": "CONFIGURACIÓN",
        "lbl_language": "IDIOMA / LANGUAGE",
        "btn_test_discord": "🔔 Probar Discord",
        "btn_test_telegram": "🔔 Probar Telegram",
        "btn_test_whatsapp": "🔔 Probar WhatsApp",
        "btn_save_config": "💾 GUARDAR AJUSTES",

        # Modales y Alertas
        "modal_title": "CONFIRMACIÓN DE SEGURIDAD",
        "modal_default_msg": "¿Deseas ejecutar esta acción remota?",
        "modal_btn_execute": "EJECUTAR",
        "modal_btn_cancel": "CANCELAR",
        "modal_confirm_shutdown_title": "APAGAR SISTEMA",
        "modal_confirm_shutdown_msg": "¿Confirmas que deseas apagar el equipo remotamente?",
        "modal_confirm_reboot_title": "REINICIAR SISTEMA",
        "modal_confirm_reboot_msg": "¿Confirmas que deseas reiniciar el equipo remotamente?",
        "modal_confirm_defcon_title": "ACTIVAR MODO PANICO DEFCON-1",
        "modal_confirm_defcon_msg": "¿Confirmas el bloqueo forzoso inmediato de la estación y captura silenciosa de evidencia?",
        "modal_confirm_kill_title": "FINALIZAR PROCESO",
        "modal_confirm_kill_msg": "¿Deseas cerrar la tarea {name} (PID: {pid})?",

        # Toasts
        "toast_broadcasting_report": "Transmitiendo reporte a canales...",
        "toast_sending_evidence": "Transmitiendo evidencia a canales...",
        "toast_compiling_video": "Compilando video forense desde memoria RAM...",
        "toast_video_ready": "Video listo",
        "toast_video_error": "Error al compilar video",
        "toast_defcon_firing": "DISPARANDO BLOQUEO DEFCON-1...",
        "toast_defcon_done": "DEFCON-1 EJECUTADO",
        "toast_defcon_error": "Error al ejecutar DEFCON-1",
        "toast_locking": "Bloqueando sesión...",
        "toast_sleeping": "Suspendiendo PC...",
        "toast_shutting_down": "Apagando en 10s...",
        "toast_rebooting": "Reiniciando equipo en 10s...",
        "toast_waking_screen": "Encendiendo pantalla...",
        "toast_sending_wol": "Enviando paquete WoL...",
        "toast_toggling_audio": "Alternando audio...",
        "toast_setting_volume": "Fijando volumen al 50%...",
        "toast_cancelling": "Cancelando apagado/reinicio...",
        "toast_killing": "Cerrando {name}...",
        "toast_testing_channel": "Enviando prueba a {channel}...",
        "toast_saving_settings": "Guardando ajustes...",
        "toast_settings_saved": "Ajustes guardados con éxito",
        "toast_settings_error": "Error al guardar ajustes",
        "toast_fetch_media": "Obteniendo {label}...",
        "toast_comm_error": "Error de comunicación con el servidor"
    }
}


def normalize_lang(lang: str) -> str:
    """Normalizes language code to supported set, defaulting to DEFAULT_LANGUAGE."""
    if not lang:
        return DEFAULT_LANGUAGE
    code = lang.lower().strip()[:2]
    return code if code in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


def t(key: str, lang: str = None, **kwargs: Any) -> str:
    """
    Translates a message key into the requested language with optional keyword formatting.
    Falls back to English if key is missing in target language.
    """
    selected_lang = normalize_lang(lang)
    entry = MESSAGES.get(key)
    
    if not entry:
        return key

    text = entry.get(selected_lang) or entry.get("en") or entry.get("es") or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


def get_web_translations(lang: str = None) -> Dict[str, str]:
    """Returns the translation dictionary for the web dashboard."""
    selected_lang = normalize_lang(lang)
    return WEB_TRANSLATIONS.get(selected_lang, WEB_TRANSLATIONS["en"])
