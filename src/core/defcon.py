# -*- coding: utf-8 -*-
"""
OpenSentinel DEFCON-1 Panic Protocol
1-Click silent forensic capture, instant workstation lock, and audio silencing.
"""

import ctypes
import datetime
import io
import threading
from PIL import Image, ImageDraw
from .surveillance import get_shared_webcam_frame

LAST_DEFCON_TIME = None
LAST_DEFCON_PHOTO = None
DEFCON_LOCK = threading.Lock()

def trigger_defcon_panic() -> dict:
    """Ejecuta el protocolo de pánico DEFCON-1 en 1 milisegundo."""
    global LAST_DEFCON_TIME, LAST_DEFCON_PHOTO

    # 1. Foto silenciosa instantánea desde la memoria RAM de la webcam
    photo_bytes = None
    raw_frame = get_shared_webcam_frame()
    if raw_frame is not None:
        try:
            import cv2
            _, b = cv2.imencode(".jpg", raw_frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            photo_bytes = b.tobytes()
            with DEFCON_LOCK:
                LAST_DEFCON_PHOTO = photo_bytes
                LAST_DEFCON_TIME = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        except Exception:
            pass

    # 2. Bloquear estación de Windows inmediatamente
    ctypes.windll.user32.LockWorkStation()

    # 3. Silenciar audio del hardware
    ctypes.windll.user32.keybd_event(0xAD, 0, 0, 0)
    ctypes.windll.user32.keybd_event(0xAD, 0, 2, 0)

    return {
        "success": True,
        "msg": "DEFCON-1 EJECUTADO: Estacion bloqueada y evidencia asegurada",
        "timestamp": LAST_DEFCON_TIME,
        "photo_captured": photo_bytes is not None,
        "photo_bytes": photo_bytes
    }

def get_last_defcon_evidence() -> tuple:
    """Retorna los bytes de la última foto y su timestamp."""
    with DEFCON_LOCK:
        return LAST_DEFCON_PHOTO, LAST_DEFCON_TIME

def get_defcon_placeholder_bytes() -> io.BytesIO:
    """Genera una imagen placeholder si no hay registros DEFCON."""
    img = Image.new("RGB", (640, 360), color=(10, 14, 23))
    d = ImageDraw.Draw(img)
    d.text((200, 160), "SIN REGISTROS DEFCON PREVIOS", fill=(148, 163, 184))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf
