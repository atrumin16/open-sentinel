# -*- coding: utf-8 -*-
"""
OpenSentinel Interactive Configuration Wizard
Guides any user step-by-step to configure their server name, ports,
and notification channels (Discord, Telegram, WhatsApp) with zero hardcoded assumptions.
"""

import os
import sys
import time
from pathlib import Path
from ..config import load_config, save_config, CONFIG_FILE
from .hardware import get_full_hardware_summary, get_current_user
from .network import get_network_summary

def prompt_input(question: str, default: str = "") -> str:
    """Solicita un valor al usuario con un valor por defecto."""
    if default:
        res = input(f"  {question} [{default}]: ").strip()
        return res if res else default
    else:
        return input(f"  {question}: ").strip()

def prompt_bool(question: str, default: bool = True) -> bool:
    """Solicita una confirmación sí/no al usuario."""
    hint = "S/n" if default else "s/N"
    res = input(f"  {question} [{hint}]: ").strip().lower()
    if not res:
        return default
    return res in ("s", "si", "y", "yes", "true", "1")

def run_interactive_wizard():
    """Ejecuta el asistente interactivo de configuración de OpenSentinel."""
    os.system("cls" if os.name == "nt" else "clear")
    print(r"""
 ================================================================
   ___                   ____             _   _            _ 
  / _ \ _ __   ___ _ __ / ___|  ___ _ __ | |_(_)_ __   ___| |
 | | | | '_ \ / _ \ '_ \\___ \ / _ \ '_ \| __| | '_ \ / _ \ |
 | |_| | |_) |  __/ | | |___) |  __/ | | | |_| | | | |  __/ |
  \___/| .__/ \___|_| |_|____/ \___|_| |_|\__|_|_| |_|\___|_|
       |_|                                                   
          ASISTENTE INTERACTIVO DE CONFIGURACION // v1.0
          Engineered by Alberto Trujillo & Claude (Anthropic)
 ================================================================
    """)

    cfg = load_config()
    hw = get_full_hardware_summary()
    net = get_network_summary(port=cfg.get("PORT", 8888), wait_tailscale=False)

    print(" [1/5] TELEMETRIA DETECTADA EN TU SISTEMA:")
    print(f"   • Usuario Activo:  {hw['user']}")
    print(f"   • Equipo/Host:     {hw['hostname']}")
    print(f"   • Procesador:      {hw['cpu']}")
    print(f"   • Grafica:         {hw['gpu']}")
    print(f"   • Memoria RAM:     {hw['ram']['total_gb']} GB")
    print(f"   • IP Local (LAN):  {net['local_lan_ip']}")
    if net["tailscale_ip"]:
        print(f"   • IP Tailscale:    {net['tailscale_ip']} (P2P Activo)")
    else:
        print(f"   • IP Tailscale:    No detectada (Instala Tailscale si deseas acceso fuera de casa)")
    print(" ----------------------------------------------------------------")
    print()

    # 1. Ajustes del Servidor
    print(" [2/5] CONFIGURACION BASICA DEL SERVIDOR:")
    default_name = cfg.get("SERVER_NAME") or f"OpenSentinel // {hw['hostname']}"
    server_name = prompt_input("Nombre identificador de este equipo", default=default_name)
    
    port_str = prompt_input("Puerto para el panel web", default=str(cfg.get("PORT", 8888)))
    try:
        port = int(port_str)
    except ValueError:
        port = 8888

    auto_boot = prompt_bool("¿Enviar alerta automatica a los canales en cada inicio de Windows?", default=cfg.get("AUTO_ALERT_ON_BOOT", True))
    print()

    # 2. Discord
    print(" [3/5] CANAL DE ALERTAS DISCORD (RECOMENDADO):")
    print("   💡 GUIA RAPIDA DISCORD:")
    print("      1. En tu servidor Discord: Canal de texto -> Editar Canal (engranaje) -> Integraciones.")
    print("      2. Haz clic en 'Crear Webhook' -> 'Copiar URL de Webhook'.")
    discord_enabled = prompt_bool("¿Deseas activar alertas en Discord?", default=cfg.get("DISCORD_ENABLED", True))
    discord_url = cfg.get("DISCORD_WEBHOOK_URL", "")
    discord_thread = cfg.get("DISCORD_THREAD_ID", "")

    if discord_enabled:
        discord_url = prompt_input("URL del Webhook de Discord (https://discord.com/api/webhooks/...)", default=discord_url)
        discord_thread = prompt_input("ID del Hilo/Thread de Discord (Opcional, pulsar Enter para omitir)", default=discord_thread)

        if discord_url and discord_url.startswith("http"):
            if prompt_bool("¿Deseas enviar un mensaje de prueba a Discord ahora?", default=True):
                print("   ⏳ Transmitiendo mensaje de prueba a Discord...")
                from ..notifiers.discord import DiscordNotifier
                test_cfg = cfg.copy()
                test_cfg.update({
                    "SERVER_NAME": server_name,
                    "DISCORD_ENABLED": True,
                    "DISCORD_WEBHOOK_URL": discord_url,
                    "DISCORD_THREAD_ID": discord_thread
                })
                notifier = DiscordNotifier(test_cfg)
                res = notifier.send_test_message()
                if res.get("success"):
                    print("   ✅ [EXITO] ¡Mensaje de prueba recibido en Discord correctamente!")
                else:
                    print(f"   ⚠️ [AVISO] No se pudo entregar el mensaje: {res.get('msg')}")
    print()

    # 3. Telegram
    print(" [4/5] CANALES DE ALERTAS TELEGRAM & WHATSAPP (OPCIONALES):")
    print("   💡 GUIA RAPIDA TELEGRAM:")
    print("      1. Abre Telegram y busca @BotFather -> envía /newbot para obtener el TOKEN.")
    print("      2. Busca @userinfobot en Telegram -> envía /start para ver tu Chat ID.")
    telegram_enabled = prompt_bool("¿Deseas activar alertas por Telegram?", default=cfg.get("TELEGRAM_ENABLED", False))
    telegram_token = cfg.get("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id = cfg.get("TELEGRAM_CHAT_ID", "")

    if telegram_enabled:
        telegram_token = prompt_input("Token del Bot de Telegram (ej. 123456:ABC-DEF...)", default=telegram_token)
        telegram_chat_id = prompt_input("Chat ID del destinatario en Telegram", default=telegram_chat_id)
        if telegram_token and telegram_chat_id:
            if prompt_bool("¿Deseas enviar un mensaje de prueba a Telegram?", default=True):
                from ..notifiers.telegram import TelegramNotifier
                test_cfg = cfg.copy()
                test_cfg.update({
                    "SERVER_NAME": server_name,
                    "TELEGRAM_ENABLED": True,
                    "TELEGRAM_BOT_TOKEN": telegram_token,
                    "TELEGRAM_CHAT_ID": telegram_chat_id
                })
                res = TelegramNotifier(test_cfg).send_test_message()
                print(f"   {'✅' if res.get('success') else '⚠️'} {res.get('msg')}")

    print("   💡 GUIA RAPIDA WHATSAPP (CallMeBot):")
    print("      1. Guarda en contactos: +34 644 10 55 84.")
    print("      2. Envía por WhatsApp: 'I allow callmebot to send me messages'.")
    print("      3. Recibirás tu API Key en 10 segundos.")
    whatsapp_enabled = prompt_bool("¿Deseas activar alertas por WhatsApp?", default=cfg.get("WHATSAPP_ENABLED", False))
    wa_phone = cfg.get("WHATSAPP_PHONE", "")
    wa_key = cfg.get("WHATSAPP_API_KEY", "")
    wa_url = cfg.get("WHATSAPP_WEBHOOK_URL", "")

    if whatsapp_enabled:
        wa_provider = prompt_input("Proveedor de WhatsApp ('callmebot' o 'webhook')", default=cfg.get("WHATSAPP_PROVIDER", "callmebot"))
        if wa_provider.lower() == "callmebot":
            wa_phone = prompt_input("Numero de telefono con prefijo internacional (ej. +34600000000)", default=wa_phone)
            wa_key = prompt_input("API Key de CallMeBot", default=wa_key)
        else:
            wa_url = prompt_input("URL del Webhook de WhatsApp", default=wa_url)
    else:
        wa_provider = "callmebot"
    print()

    # 4. Seguridad y Funcionalidades
    print(" [5/5] MODULOS DE SEGURIDAD & FORENSE:")
    enable_screenshot = prompt_bool("¿Habilitar captura de pantalla en RAM para el panel?", default=cfg.get("ENABLE_SCREENSHOT", True))
    enable_webcam = prompt_bool("¿Habilitar sensor de camara web / auditoria forense?", default=cfg.get("ENABLE_WEBCAM", True))
    enable_cmd = prompt_bool("¿Permitir ejecucion remota de comandos de terminal desde el panel?", default=cfg.get("ENABLE_CMD_EXECUTION", True))
    print()

    # Guardar configuración
    new_cfg = {
        "SERVER_NAME": server_name,
        "PORT": port,
        "HOST": "0.0.0.0",
        "AUTO_ALERT_ON_BOOT": auto_boot,
        "DISCORD_ENABLED": discord_enabled,
        "DISCORD_WEBHOOK_URL": discord_url,
        "DISCORD_THREAD_ID": discord_thread,
        "TELEGRAM_ENABLED": telegram_enabled,
        "TELEGRAM_BOT_TOKEN": telegram_token,
        "TELEGRAM_CHAT_ID": telegram_chat_id,
        "WHATSAPP_ENABLED": whatsapp_enabled,
        "WHATSAPP_PROVIDER": wa_provider,
        "WHATSAPP_PHONE": wa_phone,
        "WHATSAPP_API_KEY": wa_key,
        "WHATSAPP_WEBHOOK_URL": wa_url,
        "ENABLE_WEBCAM": enable_webcam,
        "ENABLE_SCREENSHOT": enable_screenshot,
        "ENABLE_CMD_EXECUTION": enable_cmd
    }

    save_config(new_cfg)
    print(" ================================================================")
    print(" ✅ CONFIGURACION GUARDADA CON EXITO EN 'config.json'")
    print(" ================================================================")
    print(f"  • Servidor:          {server_name}")
    print(f"  • Puerto Local:      http://127.0.0.1:{port}")
    print(f"  • Red LAN:           http://{net['local_lan_ip']}:{port}")
    if net["tailscale_ip"]:
        print(f"  • Enlace Tailscale:  http://{net['tailscale_ip']}:{port}")
    print(" ================================================================")
    print(" 🚀 PROXIMOS PASOS:")
    print("  • Iniciar en segundo plano:   Haz doble clic en scripts/start.bat")
    print("  • Detener en cualquier momento: Haz doble clic en scripts/stop.bat")
    print("  • Reconfigurar opciones:       Haz doble clic en scripts/setup.bat")
    print(" ================================================================")
    print()
