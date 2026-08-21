# -*- coding: utf-8 -*-
r"""
================================================================================
  ___                   ____             _   _            _ 
 / _ \ _ __   ___ _ __ / ___|  ___ _ __ | |_(_)_ __   ___| |
| | | | '_ \ / _ \ '_ \\___ \ / _ \ '_ \| __| | '_ \ / _ \ |
| |_| | |_) |  __/ | | |___) |  __/ | | | |_| | | | |  __/ |
 \___/| .__/ \___|_| |_|____/ \___|_| |_|\__|_|_| |_|\___|_|
      |_|                                                   
Open-Source PC Telemetry, Multi-Channel Boot Alerts & Forensics
================================================================================
"""

import argparse
import sys
import threading
from src.config import load_config
from src.core.surveillance import start_surveillance_threads
from src.core.network import get_network_summary
from src.notifiers.dispatcher import dispatch_boot_alert, send_test_notification
from src.web.app import create_app, check_single_instance

def print_banner(cfg: dict, net: dict):
    port = cfg.get("PORT", 8888)
    name = cfg.get("SERVER_NAME", "OpenSentinel")
    print(r"""
   ___                   ____             _   _            _ 
  / _ \ _ __   ___ _ __ / ___|  ___ _ __ | |_(_)_ __   ___| |
 | | | | '_ \ / _ \ '_ \\___ \ / _ \ '_ \| __| | '_ \ / _ \ |
 | |_| | |_) |  __/ | | |___) |  __/ | | | |_| | | | |  __/ |
  \___/| .__/ \___|_| |_|____/ \___|_| |_|\__|_|_| |_|\___|_|
       |_|                                                   
    """)
    print(f"============================================================")
    print(f"  {name} v1.0.0 // NODO ACTIVO")
    print(f"  • Acceso Local:      http://127.0.0.1:{port}")
    print(f"  • Acceso LAN:        {net['url_local']}")
    if net['tailscale_ip']:
        print(f"  • Acceso Remoto:     {net['url_remote']} (Tailscale P2P)")
    print(f"  • Canales Activos:   "
          f"Discord [{'OK' if cfg.get('DISCORD_ENABLED') else 'OFF'}] | "
          f"Telegram [{'OK' if cfg.get('TELEGRAM_ENABLED') else 'OFF'}] | "
          f"WhatsApp [{'OK' if cfg.get('WHATSAPP_ENABLED') else 'OFF'}]")
    print(f"============================================================")

def main():
    parser = argparse.ArgumentParser(description="OpenSentinel Server & Alerter")
    parser.add_argument("--alert-only", action="store_true", help="Send boot alert and exit")
    parser.add_argument("--force-alert", action="store_true", help="Force send boot alert bypassing anti-spam")
    parser.add_argument("--test-notifiers", action="store_true", help="Send test pings to all active notification channels")
    parser.add_argument("--port", type=int, help="Override server port")
    args = parser.parse_args()

    cfg = load_config()
    if args.port:
        cfg["PORT"] = args.port

    # Test de canales
    if args.test_notifiers:
        print("[TEST] Probando canales de notificacion...")
        for ch in ("discord", "telegram", "whatsapp"):
            res = send_test_notification(ch, cfg)
            print(f"  • {ch.capitalize()}: {res['msg']}")
        return

    # Modo solo alerta de inicio
    if args.alert_only:
        print("[BOOT] Ejecutando envio de alerta...")
        res = dispatch_boot_alert(force=args.force_alert)
        print(f"[BOOT] {res['msg']}")
        return

    # Comprobar instancia única
    port = cfg.get("PORT", 8888)
    if not check_single_instance(port):
        print(f"[AVISO] Ya existe una instancia de OpenSentinel ejecutandose en el puerto {port}.")
        sys.exit(0)

    # Iniciar grabación forense en RAM
    start_surveillance_threads(
        enable_webcam=cfg.get("ENABLE_WEBCAM", True),
        enable_screenshot=cfg.get("ENABLE_SCREENSHOT", True)
    )

    # Disparar alerta inteligente de inicio en segundo plano
    if cfg.get("AUTO_ALERT_ON_BOOT", True):
        threading.Thread(target=dispatch_boot_alert, kwargs={"force": args.force_alert}, daemon=True).start()

    net = get_network_summary(port=port)
    print_banner(cfg, net)

    # Iniciar servidor Web Flask
    app = create_app()
    app.run(host=cfg.get("HOST", "0.0.0.0"), port=port, debug=False)

if __name__ == "__main__":
    main()
