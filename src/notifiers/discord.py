# -*- coding: utf-8 -*-
"""
OpenSentinel Discord Notifier
Sends clean executive embeds and forensic photos via Discord Webhooks.
"""

import datetime
import json
import requests
from .base import BaseNotifier
from ..i18n import t

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
        lang = self.config.get("LANGUAGE", "en")
        iso_timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        url_remote = net.get("url_remote", "")
        url_local = net.get("url_local") or "http://127.0.0.1:8888"

        if url_remote:
            remote_line = t("discord_remote_active", lang, url=url_remote)
        else:
            remote_line = t("discord_remote_inactive", lang)

        local_line = t("discord_local_link", lang, url=url_local)

        embed = {
            "title": t("discord_boot_title", lang, hostname=hw['hostname'].upper()),
            "description": (
                f"{t('discord_boot_desc_header', lang)}\n"
                f"{remote_line}\n"
                f"{local_line}"
            ),
            "color": 0x38BDF8,  # Cyan
            "timestamp": iso_timestamp,
            "fields": [
                {
                    "name": t("discord_field_station", lang),
                    "value": f"`{hw['user']} @ {hw['hostname']}`",
                    "inline": True
                },
                {
                    "name": t("discord_field_conn_time", lang),
                    "value": f"`{now_str}`",
                    "inline": True
                },
                {
                    "name": t("discord_field_hw", lang),
                    "value": f"• **CPU:** `{hw['cpu']}`\n• **GPU:** `{hw['gpu']}`\n• **RAM:** `{hw['ram']['total_gb']} GB`",
                    "inline": False
                },
                {
                    "name": t("discord_field_network", lang),
                    "value": f"• **{t('field_public_ip', lang)}:** `{net['public_ip']}` ({net['isp']} - {net['location']})\n• **{t('field_tailscale_ip', lang)}:** `{net['tailscale_ip'] or t('inactive', lang)}`\n• **{t('field_lan_ip', lang)}:** `{net['local_lan_ip']}`",
                    "inline": False
                }
            ],
            "footer": {
                "text": t("discord_footer_boot", lang, server_name=server_name),
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
        lang = self.config.get("LANGUAGE", "en")
        now_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        payload = {
            "username": server_name,
            "avatar_url": "https://cdn-icons-png.flaticon.com/512/906/906338.png",
            "content": t("discord_evidence_content", lang, reason=reason, time=now_str),
            "embeds": [{
                "title": title,
                "description": t("discord_evidence_desc", lang, reason=reason),
                "color": 0xF43F5E if "DEFCON" in title or "Intruso" in reason or "Intruder" in reason else 0xF59E0B,
                "image": {"url": "attachment://evidencia.jpg"},
                "footer": {"text": t("discord_evidence_footer", lang, server_name=server_name)}
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
        
        lang = self.config.get("LANGUAGE", "en")
        webhook_url = self.config.get("DISCORD_WEBHOOK_URL", "").strip()
        payload = {
            "username": self.config.get("SERVER_NAME", "OpenSentinel"),
            "content": t("discord_test_msg", lang)
        }
        try:
            resp = requests.post(webhook_url, json=payload, timeout=5)
            if resp.status_code in (200, 204):
                return {"success": True, "msg": "Mensaje de prueba enviado a Discord con exito"}
            return {"success": False, "msg": f"Discord respondio con codigo {resp.status_code}: {resp.text}"}
        except Exception as e:
            return {"success": False, "msg": f"Error al conectar con Discord: {e}"}
