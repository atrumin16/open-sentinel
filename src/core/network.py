# -*- coding: utf-8 -*-
"""
OpenSentinel Network Discovery & Telemetry Module
Detects Tailscale, Local LAN, Public IP, Geo-location, and WoL capabilities.
"""

import os
import shutil
import socket
import subprocess
import psutil
import requests

def get_tailscale_ip(retries: int = 1, delay: float = 2.0) -> str:
    """Obtiene la dirección IPv4 de la interfaz Tailscale P2P si está activa."""
    import time
    for _ in range(max(1, retries)):
        try:
            ts_cmd = shutil.which("tailscale") or r"C:\Program Files\Tailscale\tailscale.exe"
            if os.path.exists(ts_cmd):
                out = subprocess.check_output([ts_cmd, "ip", "-4"], text=True, stderr=subprocess.DEVNULL, timeout=3).strip()
                if out and not out.startswith("169.254") and out.startswith("100."):
                    return out
        except Exception:
            pass

        # Búsqueda por adaptador de red
        try:
            for iface, addrs in psutil.net_if_addrs().items():
                if "tailscale" in iface.lower():
                    for addr in addrs:
                        if addr.family == socket.AF_INET and not addr.address.startswith("169.254"):
                            return addr.address
        except Exception:
            pass
        if retries > 1:
            time.sleep(delay)
    return ""

def get_local_lan_ip() -> str:
    """Obtiene la dirección IPv4 del adaptador LAN activo conectado a la red local."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def get_public_ip_info() -> dict:
    """Obtiene la IP pública externa, ISP y geolocalización."""
    try:
        geo = requests.get("http://ip-api.com/json/?fields=status,country,city,isp,query", timeout=3).json()
        if geo.get("status") == "success":
            return {
                "ip": geo.get("query", "Desconocida"),
                "city": geo.get("city", ""),
                "country": geo.get("country", ""),
                "location": f"{geo.get('city')}, {geo.get('country')}",
                "isp": geo.get("isp", "Proveedor de Internet")
            }
    except Exception:
        pass

    try:
        ip = requests.get("https://api.ipify.org", timeout=2).text.strip()
        return {"ip": ip, "city": "", "country": "", "location": "Ubicacion no disponible", "isp": "Internet"}
    except Exception:
        return {"ip": "Desconocida", "city": "", "country": "", "location": "Desconocida", "isp": "Desconocido"}

def send_wol_packet() -> bool:
    """Envía un paquete mágico Wake-on-LAN (WoL) en broadcast para reactivar nodos."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(b'\xff' * 102, ("255.255.255.255", 9))
        s.close()
        return True
    except Exception:
        return False

def get_network_summary(port=8888, wait_tailscale=False) -> dict:
    """Genera un resumen completo de enlaces de red y URLs de acceso."""
    ts_ip = get_tailscale_ip(retries=18, delay=2.0) if wait_tailscale else get_tailscale_ip()
    lan_ip = get_local_lan_ip()
    pub = get_public_ip_info()

    return {
        "tailscale_ip": ts_ip,
        "local_lan_ip": lan_ip,
        "public_ip": pub["ip"],
        "isp": pub["isp"],
        "location": pub["location"],
        "url_remote": f"http://{ts_ip}:{port}" if ts_ip else "",
        "url_local": f"http://{lan_ip}:{port}",
        "url_loopback": f"http://127.0.0.1:{port}"
    }

def is_trusted_ip(ip: str) -> bool:
    """Valida si una dirección IP pertenece a la red local privada o a la malla P2P de Tailscale."""
    if not ip:
        return False
    return (
        ip.startswith("100.") or
        ip.startswith("192.168.") or
        ip.startswith("10.") or
        ip.startswith("172.") or
        ip in ("127.0.0.1", "::1", "localhost")
    )
