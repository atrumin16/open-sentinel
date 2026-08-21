# -*- coding: utf-8 -*-
"""
OpenSentinel Telegram Bot Notifier
Sends alerts and forensic photos directly to personal chats or Telegram groups.
"""

import datetime
import requests
from .base import BaseNotifier

class TelegramNotifier(BaseNotifier):
    def is_enabled(self) -> bool:
        token = self.config.get("TELEGRAM_BOT_TOKEN", "").strip()
        chat_id = str(self.config.get("TELEGRAM_CHAT_ID", "")).strip()
        enabled = self.config.get("TELEGRAM_ENABLED", False)
        return bool(enabled and token and chat_id)

    def _get_api_url(self, method: str) -> str:
        token = self.config.get("TELEGRAM_BOT_TOKEN", "").strip()
        return f"https://api.telegram.org/bot{token}/{method}"

    def send_boot_alert(self, hw: dict, net: dict) -> bool:
        if not self.is_enabled():
            return False

        chat_id = str(self.config.get("TELEGRAM_CHAT_ID", "")).strip()
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        url_remote = net.get("url_remote") or "Inactiva (Sin Tailscale)"
        url_local = net.get("url_local") or "http://127.0.0.1:8888"

        text = (
            f"🟢 *[OPENSENTINEL]* Nodo en Línea\n\n"
            f"💻 *Estación:* `{hw['user']} @ {hw['hostname']}`\n"
            f"⏱️ *Hora:* `{now_str}`\n"
            f"⚡ *Hardware:* `{hw['cpu']}` | `{hw['gpu']}` | `{hw['ram']['total_gb']} GB RAM`\n"
            f"🌐 *Red:* `{net['public_ip']}` ({net['isp']} - {net['location']})\n\n"
            f"🔗 *ACCESO AL PANEL:*\n"
            f"• [Panel Remoto (Tailscale)]({url_remote})\n"
            f"• [Panel Local (LAN)]({url_local})"
        )

        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False
        }

        try:
            resp = requests.post(self._get_api_url("sendMessage"), json=payload, timeout=8)
            return resp.status_code == 200
        except Exception as e:
            print(f"[ERROR Telegram] {e}")
            return False

    def send_evidence_alert(self, img_bytes: bytes, title: str, reason: str) -> bool:
        if not self.is_enabled() or not img_bytes:
            return False

        chat_id = str(self.config.get("TELEGRAM_CHAT_ID", "")).strip()
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        caption = f"🚨 *[{title}]*\n\n📋 *Motivo:* {reason}\n⏱️ *Hora:* `{now_str}`\n🛡️ *Estado:* Evidencia capturada desde RAM"

        files = {
            "photo": ("evidencia.jpg", img_bytes, "image/jpeg")
        }
        data = {
            "chat_id": chat_id,
            "caption": caption,
            "parse_mode": "Markdown"
        }

        try:
            resp = requests.post(self._get_api_url("sendPhoto"), data=data, files=files, timeout=10)
            return resp.status_code == 200
        except Exception as e:
            print(f"[ERROR Telegram Evidence] {e}")
            return False

    def send_test_message(self) -> dict:
        if not self.is_enabled():
            return {"success": False, "msg": "Telegram no esta habilitado o falta Token / Chat ID"}

        chat_id = str(self.config.get("TELEGRAM_CHAT_ID", "")).strip()
        payload = {
            "chat_id": chat_id,
            "text": "🔔 *[OpenSentinel]* Mensaje de prueba recibido correctamente en Telegram.",
            "parse_mode": "Markdown"
        }

        try:
            resp = requests.post(self._get_api_url("sendMessage"), json=payload, timeout=6)
            if resp.status_code == 200:
                return {"success": True, "msg": "Mensaje de prueba enviado a Telegram con exito"}
            return {"success": False, "msg": f"Telegram respondio con error {resp.status_code}: {resp.text}"}
        except Exception as e:
            return {"success": False, "msg": f"Error al conectar con Telegram: {e}"}
