# -*- coding: utf-8 -*-
"""
OpenSentinel Hardware & System Telemetry Detector
Queries dynamic hardware specs without hardcoding any computer information.
"""

import ctypes
import datetime
import os
import platform
import subprocess
import psutil

def get_cpu_name() -> str:
    """Obtiene el nombre comercial del procesador."""
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
        name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
        return name.strip()
    except Exception:
        return platform.processor() or "Procesador x64"

def get_gpu_name() -> str:
    """Obtiene el nombre de la tarjeta gráfica dedicada o integrada."""
    try:
        out = subprocess.check_output("wmic path win32_VideoController get name", shell=True, text=True, stderr=subprocess.DEVNULL)
        lines = [line.strip() for line in out.splitlines() if line.strip() and "Name" not in line]
        valid = [l for l in lines if "virtual" not in l.lower() and "basic" not in l.lower()]
        return valid[0] if valid else (lines[0] if lines else "Gráficos Integrados / GPU")
    except Exception:
        return "GPU del Sistema"

def get_ram_stats() -> dict:
    """Retorna desglose de memoria RAM física."""
    mem = psutil.virtual_memory()
    total_gb = round(mem.total / (1024**3), 1)
    used_gb = round((mem.total - mem.available) / (1024**3), 1)
    free_gb = round(mem.available / (1024**3), 1)
    return {
        "total_gb": total_gb,
        "used_gb": used_gb,
        "free_gb": free_gb,
        "pct": mem.percent
    }

def get_disks_stats() -> list:
    """Retorna información de todas las unidades de almacenamiento fijas."""
    disks = []
    for part in psutil.disk_partitions(all=False):
        if "fixed" in part.opts or "rw" in part.opts:
            try:
                usage = psutil.disk_usage(part.mountpoint)
                disks.append({
                    "drive": part.mountpoint,
                    "total_gb": round(usage.total / (1024**3), 1),
                    "free_gb": round(usage.free / (1024**3), 1),
                    "used_gb": round(usage.used / (1024**3), 1),
                    "pct": usage.percent
                })
            except Exception:
                continue
    return disks

def get_system_uptime() -> dict:
    """Retorna el tiempo de actividad del sistema operativo."""
    boot_ts = psutil.boot_time()
    boot_dt = datetime.datetime.fromtimestamp(boot_ts)
    delta = datetime.datetime.now() - boot_dt
    hours, rem = divmod(int(delta.total_seconds()), 3600)
    mins, secs = divmod(rem, 60)
    uptime_str = f"{delta.days}d {hours}h {mins}m"
    return {
        "boot_timestamp": int(boot_ts),
        "boot_datetime": boot_dt.strftime("%d/%m/%Y %H:%M:%S"),
        "uptime_str": uptime_str,
        "days": delta.days,
        "hours": hours,
        "minutes": mins
    }

def get_active_window_title() -> str:
    """Obtiene el título de la ventana activa en primer plano en Windows."""
    try:
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        if hwnd == 0:
            return "Escritorio / Bloqueado"
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff.value or "Escritorio / Bloqueado"
    except Exception:
        return "Escritorio"

def get_full_hardware_summary() -> dict:
    """Genera un resumen consolidado del hardware del equipo."""
    ram = get_ram_stats()
    uptime = get_system_uptime()
    return {
        "hostname": platform.node(),
        "user": os.getenv("USERNAME", "Usuario"),
        "os": f"{platform.system()} {platform.release()} ({platform.version()})",
        "cpu": get_cpu_name(),
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
        "gpu": get_gpu_name(),
        "ram": ram,
        "disks": get_disks_stats(),
        "uptime": uptime,
        "active_window": get_active_window_title()
    }
