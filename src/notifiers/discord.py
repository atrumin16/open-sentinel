# -*- coding: utf-8 -*-
"""
OpenSentinel Discord Notifier
Sends clean executive embeds and forensic photos via Discord Webhooks.
"""

import datetime
import json
import requests
from .base import BaseNotifier

class DiscordNotifier(BaseNotifier):
    def is_enabled(self) -> bool:
        url = self.config.get("DISCORD_WEBHOOK_URL", "").strip()
        enabled = self.config.get("DISCORD_ENABLED", True)
        return bool(enabled and url and url.startswith("http"))

    def send_boot_alert(self, hw: dict, net: dict) -> bool:
        if not self.is_enabled():
            return False

        webhook_url = self.config.get("DISCORD_WEBHOOK_URL", "").strip()
        thread_id = self.config.get("DISCORD_THREAD_ID", "").strip()
        server_name = self.config.get("SERVER_NAME", "OpenSentinel")
        iso_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        url_remote = net.get("url_remote", "")
        url_local = net.get("url_local") or "http://127.0.0.1:8888"

        if url_remote:
            remote_line = f"• 🚀 **Acceso Remoto (Tailscale P2P):** [Abrir Panel Remoto]({url_remote})"
        else:
            remote_line = "• 🚀 **Acceso Remoto (Tailscale P2P):** *No disponible en el arranque*"

        local_line = f"• 🏠 **Acceso Local (Red Doméstica LAN):** [Abrir Panel Local]({url_local})"

        embed = {
            "title": f"🟢 SISTEMA EN LÍNEA // {hw['hostname'].upper()}",
            "description": (
                f"**CENTRO DE CONTROL REMOTO DISPONIBLE:**\n"
                f"{remote_line}\n"
                f"{local_line}"
            ),
            "color": 0x38BDF8,  # Azul Cyan
            "timestamp": iso_timestamp,
            "fields": [
                {
                    "name": "💻 Estación & Usuario",
                    "value": f"`{hw['user']} @ {hw['hostname']}`",
                    "inline": True
                },
                {
                    "name": "⏱️ Hora de Conexión",
                    "value": f"`{now_str}`",
                    "inline": True
                },
                {
                    "name": "⚡ Especificaciones de Hardware",
                    "value": f"• **CPU:** `{hw['cpu']}`\n• **GPU:** `{hw['gpu']}`\n• **RAM:** `{hw['ram']['total_gb']} GB`",
                    "inline": False
                },
                {
                    "name": "🌐 Red & Enlace de Seguridad",
                    "value": f"• **IP Pública:** `{net['public_ip']}` ({net['isp']} - {net['location']})\n• **IP Tailscale:** `{net['tailscale_ip'] or 'Inactiva'}`\n• **IP LAN:** `{net['local_lan_ip']}`",
                    "inline": False
                }
            ],
            "footer": {
                "text": f"{server_name} • Sesión de Inicio Verificada",
                "icon_url": "https://cdn-icons-png.flaticon.com/512/906/906338.png"
            }
        }

        payload = {
            "username": server_name,
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/906/906338.png",
            "embeds": [embed]
        }

        target_url = f"{webhook_url}?thread_id={thread_id}" if thread_id else webhook_url

        try:
            resp = requests.post(target_url, json=payload, headers={"Content-Type": "application/json"}, timeout=8)
            if resp.status_code in (400, 404) and thread_id:
                resp = requests.post(webhook_url, json=payload, headers={"Content-Type": "application/json"}, timeout=8)
            return resp.status_code in (200, 204)
        except Exception as e:
            print(f"[ERROR Discord] {e}")
            return False

    def send_evidence_alert(self, img_bytes: bytes, title: str, reason: str) -> bool:
        if not self.is_enabled() or not img_bytes:
            return False

        webhook_url = self.config.get("DISCORD_WEBHOOK_URL", "").strip()
        thread_id = self.config.get("DISCORD_THREAD_ID", "").strip()
        server_name = self.config.get("SERVER_NAME", "OpenSentinel")
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        payload = {
            "username": server_name,
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/906/906338.png",
            "content": f"### [SENTINEL // AUDITORÍA FORENSE] {reason}\n> **Hora:** `{now_str}`",
            "embeds": [{
                "title": title,
                "description": f"**Motivo:** {reason}\n**Seguridad:** Evidencia capturada desde RAM.",
                "color": 0xF43F5E if "DEFCON" in title or "Intruso" in reason else 0xF59E0B,
                "image": {"url": "attachment://evidencia.jpg"},
                "footer": {"text": f"{server_name} | Registro Forense"}
            }]
        }

        files = {
            "payload_json": (None, json.dumps(payload), "application/json"),
            "files[0]": ("evidencia.jpg", img_bytes, "image/jpeg")
        }

        target_url = f"{webhook_url}?thread_id={thread_id}" if thread_id else webhook_url

        try:
            resp = requests.post(target_url, files=files, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            if resp.status_code in (400, 404) and thread_id:
                resp = requests.post(webhook_url, files=files, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            return resp.status_code in (200, 204)
        except Exception as e:
            print(f"[ERROR Discord Evidence] {e}")
            return False

    def send_test_message(self) -> dict:
        if not self.is_enabled():
            return {"success": False, "msg": "Discord no esta habilitado o falta la URL del Webhook"}
        
        webhook_url = self.config.get("DISCORD_WEBHOOK_URL", "").strip()
        payload = {
            "username": self.config.get("SERVER_NAME", "OpenSentinel"),
            "content": "🔔 **[OpenSentinel]** Mensaje de prueba recibido correctamente desde el panel de control."
        }
        try:
            resp = requests.post(webhook_url, json=payload, timeout=5)
            if resp.status_code in (200, 204):
                return {"success": True, "msg": "Mensaje de prueba enviado a Discord con exito"}
            return {"success": False, "msg": f"Discord respondio con codigo {resp.status_code}: {resp.text}"}
        except Exception as e:
            return {"success": False, "msg": f"Error al conectar con Discord: {e}"}
