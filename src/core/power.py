# -*- coding: utf-8 -*-
"""
OpenSentinel Power & Session Control Module
Lock workstation, S3 sleep, scheduled reboot/shutdown, abort, screen wake, audio.
"""

import ctypes
import os
import subprocess

def lock_workstation() -> bool:
    """Bloquea la sesión de usuario de Windows."""
    try:
        ctypes.windll.user32.LockWorkStation()
        return True
    except Exception:
        return False

def sleep_system() -> bool:
    """Pone el equipo en estado de suspensión S3."""
    try:
        os.system('powershell -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState([System.Windows.Forms.PowerState]::Suspend, $false, $false)"')
        return True
    except Exception:
        return False

def schedule_shutdown(seconds=10) -> bool:
    """Programa el apagado del equipo con un temporizador."""
    try:
        os.system(f"shutdown /s /t {int(seconds)} /f")
        return True
    except Exception:
        return False

def schedule_reboot(seconds=10) -> bool:
    """Programa el reinicio del equipo con un temporizador."""
    try:
        os.system(f"shutdown /r /t {int(seconds)} /f")
        return True
    except Exception:
        return False

def cancel_power_action() -> bool:
    """Cancela cualquier apagado o reinicio pendiente en Windows."""
    try:
        res = os.system("shutdown /a")
        return res == 0
    except Exception:
        return False

def wake_screen() -> bool:
    """Enciende los monitores y despierta el compositor de ventanas DWM."""
    try:
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        kernel32.SetThreadExecutionState(0x80000000 | 0x00000001 | 0x00000002)
        user32.SendMessageW(0xFFFF, 0x0112, 0xF170, -1)
        user32.keybd_event(0x10, 0, 0, 0)
        user32.keybd_event(0x10, 0, 2, 0)
        return True
    except Exception:
        return False

def toggle_mute() -> bool:
    """Silencia o reactiva la salida de audio global del hardware."""
    try:
        user32 = ctypes.windll.user32
        user32.keybd_event(0xAD, 0, 0, 0)
        user32.keybd_event(0xAD, 0, 2, 0)
        return True
    except Exception:
        return False

def set_volume_level(level: int) -> bool:
    """Fija el nivel de volumen aproximado en Windows (0 a 100)."""
    try:
        user32 = ctypes.windll.user32
        # Bajar a cero
        for _ in range(50):
            user32.keybd_event(0xAE, 0, 0, 0)
            user32.keybd_event(0xAE, 0, 2, 0)
        # Subir al porcentaje
        steps = int(max(0, min(level, 100)) / 2)
        for _ in range(steps):
            user32.keybd_event(0xAF, 0, 0, 0)
            user32.keybd_event(0xAF, 0, 2, 0)
        return True
    except Exception:
        return False

def show_screen_alert(message: str, title="OpenSentinel Alerta") -> bool:
    """Muestra una caja de diálogo de alerta en el escritorio del PC con sonido."""
    try:
        def _popup():
            ctypes.windll.user32.MessageBeep(0x00000030)
            ctypes.windll.user32.MessageBoxW(0, message, title, 0x10 | 0x40000)
        import threading
        threading.Thread(target=_popup, daemon=True).start()
        return True
    except Exception:
        return False
