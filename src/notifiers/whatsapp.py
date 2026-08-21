# -*- coding: utf-8 -*-
"""
OpenSentinel WhatsApp Notifier
Supports CallMeBot (Free personal gateway) and Custom WhatsApp Webhooks (Evolution API / Twilio).
"""

import datetime
import urllib.parse
import requests
from .base import BaseNotifier

class WhatsAppNotifier(BaseNotifier):
    def is_enabled(self) -> bool:
        enabled = self.config.get("WHATSAPP_ENABLED", False)
        provider = self.config.get("WHATSAPP_PROVIDER", "callmebot").lower()
        if not enabled:
            return False

        if provider == "callmebot":
            phone = self.config.get("WHATSAPP_PHONE", "").strip()
            apikey = self.config.get("WHATSAPP_API_KEY", "").strip()
            return bool(phone and apikey)
        elif provider in ("webhook", "evolution", "twilio"):
            url = self.config.get("WHATSAPP_WEBHOOK_URL", "").strip()
            return bool(url and url.startswith("http"))
        return False

    def send_boot_alert(self, hw: dict, net: dict) -> bool:
        if not self.is_enabled():
            return False

        provider = self.config.get("WHATSAPP_PROVIDER", "callmebot").lower()
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        url_remote = net.get("url_remote") or "Inactiva (Sin Tailscale)"
        url_local = net.get("url_local") or "http://127.0.0.1:8888"

        text = (
            f"🟢 *[OPENSENTINEL]* Nodo Online\n"
            f"💻 Estacion: {hw['user']} @ {hw['hostname']}\n"
            f"⏱️ Hora: {now_str}\n"
            f"⚡ Hardware: {hw['cpu']} | {hw['ram']['total_gb']} GB RAM\n"
            f"🌐 Red: {net['public_ip']} ({net['isp']})\n\n"
            f"🔗 Panel Remoto (Tailscale): {url_remote}\n"
            f"🏠 Panel Local (LAN): {url_local}"
        )

        if provider == "callmebot":
            phone = self.config.get("WHATSAPP_PHONE", "").strip()
            apikey = self.config.get("WHATSAPP_API_KEY", "").strip()
            encoded_text = urllib.parse.quote_plus(text)
            url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={encoded_text}&apikey={apikey}"
            try:
                resp = requests.get(url, timeout=10)
                return resp.status_code == 200
            except Exception as e:
                print(f"[ERROR WhatsApp CallMeBot] {e}")
                return False
        else:
            webhook_url = self.config.get("WHATSAPP_WEBHOOK_URL", "").strip()
            payload = {
                "message": text,
                "phone": self.config.get("WHATSAPP_PHONE", ""),
                "event": "boot_alert",
                "hostname": hw['hostname']
            }
            try:
                resp = requests.post(webhook_url, json=payload, timeout=8)
                return resp.status_code in (200, 201, 204)
            except Exception as e:
                print(f"[ERROR WhatsApp Webhook] {e}")
                return False

    def send_evidence_alert(self, img_bytes: bytes, title: str, reason: str) -> bool:
        if not self.is_enabled():
            return False

        # WhatsApp CallMeBot permite mensajes de texto con aviso
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        text = f"🚨 *[OPENSENTINEL - {title}]*\n\nMotivo: {reason}\nHora: {now_str}\nEvidencia capturada y guardada en RAM del panel."

        provider = self.config.get("WHATSAPP_PROVIDER", "callmebot").lower()
        if provider == "callmebot":
            phone = self.config.get("WHATSAPP_PHONE", "").strip()
            apikey = self.config.get("WHATSAPP_API_KEY", "").strip()
            encoded_text = urllib.parse.quote_plus(text)
            url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={encoded_text}&apikey={apikey}"
            try:
                resp = requests.get(url, timeout=10)
                return resp.status_code == 200
            except Exception:
                return False
        else:
            # Custom Webhook con soporte multipart
            webhook_url = self.config.get("WHATSAPP_WEBHOOK_URL", "").strip()
            files = {"image": ("evidencia.jpg", img_bytes, "image/jpeg")}
            data = {"caption": text, "phone": self.config.get("WHATSAPP_PHONE", "")}
            try:
                resp = requests.post(webhook_url, data=data, files=files, timeout=10)
                return resp.status_code in (200, 201, 204)
            except Exception:
                return False

    def send_test_message(self) -> dict:
        if not self.is_enabled():
            return {"success": False, "msg": "WhatsApp no esta habilitado o faltan credenciales (Phone / API Key / Webhook URL)"}

        provider = self.config.get("WHATSAPP_PROVIDER", "callmebot").lower()
        test_msg = "🔔 *[OpenSentinel]* Mensaje de prueba de WhatsApp recibido correctamente."

        if provider == "callmebot":
            phone = self.config.get("WHATSAPP_PHONE", "").strip()
            apikey = self.config.get("WHATSAPP_API_KEY", "").strip()
            encoded = urllib.parse.quote_plus(test_msg)
            url = f"https://api.callmebot.com/whatsapp.php?phone={phone}&text={encoded}&apikey={apikey}"
            try:
                resp = requests.get(url, timeout=8)
                if resp.status_code == 200:
                    return {"success": True, "msg": "Mensaje de prueba enviado a WhatsApp via CallMeBot"}
                return {"success": False, "msg": f"CallMeBot respondio con codigo {resp.status_code}: {resp.text}"}
            except Exception as e:
                return {"success": False, "msg": f"Error al conectar con WhatsApp: {e}"}
        else:
            webhook_url = self.config.get("WHATSAPP_WEBHOOK_URL", "").strip()
            payload = {"message": test_msg, "phone": self.config.get("WHATSAPP_PHONE", "")}
            try:
                resp = requests.post(webhook_url, json=payload, timeout=8)
                if resp.status_code in (200, 201, 204):
                    return {"success": True, "msg": "Mensaje de prueba enviado a WhatsApp Webhook"}
                return {"success": False, "msg": f"Webhook respondio con codigo {resp.status_code}: {resp.text}"}
            except Exception as e:
                return {"success": False, "msg": f"Error al conectar con WhatsApp Webhook: {e}"}
