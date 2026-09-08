# -*- coding: utf-8 -*-
"""
OpenSentinel Configuration Manager
Loads settings from config.json and .env with automatic fallbacks and persistence.
"""

import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.json"
BOOT_SESSION_FILE = BASE_DIR / "boot_session.json"
CLIPS_DIR = BASE_DIR / "clips"
CLIPS_DIR.mkdir(exist_ok=True)

# Cargar variables de entorno de .env si existe
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

DEFAULT_CONFIG = {
    "SERVER_NAME": "OpenSentinel",
    "PORT": 8888,
    "HOST": "0.0.0.0",
    "LANGUAGE": "en",
    "AUTO_ALERT_ON_BOOT": True,

    # Discord
    "DISCORD_ENABLED": True,
    "DISCORD_WEBHOOK_URL": "",
    "DISCORD_THREAD_ID": "",

    # Telegram
    "TELEGRAM_ENABLED": False,
    "TELEGRAM_BOT_TOKEN": "",
    "TELEGRAM_CHAT_ID": "",

    # WhatsApp
    "WHATSAPP_ENABLED": False,
    "WHATSAPP_PROVIDER": "callmebot",  # 'callmebot' | 'webhook'
    "WHATSAPP_PHONE": "",
    "WHATSAPP_API_KEY": "",
    "WHATSAPP_WEBHOOK_URL": "",

    # Security & Features
    "ENABLE_WEBCAM": True,
    "ENABLE_SCREENSHOT": True,
    "ENABLE_CMD_EXECUTION": True
}

def load_config() -> dict:
    """Carga la configuración combinando defaults, config.json y variables de entorno."""
    cfg = DEFAULT_CONFIG.copy()

    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                cfg.update(data)
        except Exception as e:
            print(f"[WARN] Error al leer {CONFIG_FILE.name}: {e}")
    else:
        # Guardar archivo por defecto si no existe
        save_config(cfg)

    # Sobrescribir con variables de entorno si están presentes
    for key in DEFAULT_CONFIG.keys():
        env_val = os.getenv(key)
        if env_val is not None:
            if isinstance(DEFAULT_CONFIG[key], bool):
                cfg[key] = env_val.lower() in ("true", "1", "yes")
            elif isinstance(DEFAULT_CONFIG[key], int):
                try: cfg[key] = int(env_val)
                except ValueError: pass
            else:
                cfg[key] = env_val

    return cfg

def save_config(new_config: dict) -> bool:
    """Guarda la configuración en config.json de manera segura."""
    try:
        current = DEFAULT_CONFIG.copy()
        current.update(new_config)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERROR] Error al guardar configuracion: {e}")
        return False
