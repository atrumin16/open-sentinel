# -*- coding: utf-8 -*-
"""
OpenSentinel In-RAM Forensic Surveillance & Capture Engine
Hardware-accelerated GDI Screen Capture • Shared Optical Sensor • Zero-Disk Video Buffer
"""

import collections
import ctypes
import datetime
import io
import os
import threading
import time
from pathlib import Path

import numpy as np
import psutil
from PIL import Image, ImageDraw

# Procesos de juegos y simulación para pausar grabación y mantener 0% CPU residual
CRITICAL_WORKLOAD_PROCESSES = {
    "iracingsim64dx11.exe", "iracingsim64.exe", "acs.exe", "assettocorsa.exe", 
    "acc.exe", "rfactor2.exe", "lemansultimate.exe", "f1_24.exe", "f1_23.exe", 
    "f1_22.exe", "eurotrucks2.exe", "amtrucks.exe", "beamng.drive.x64.exe", 
    "fortniteclient-win64-shipping.exe", "valorant.exe", "valorant-win64-shipping.exe", 
    "cs2.exe", "csgo.exe", "cyberpunk2077.exe", "forzahorizon5.exe", "blender.exe", "premiere.exe"
}

IS_OPTIMIZED_MODE = False
CURRENT_WORKLOAD_NAME = None

MAX_RAM_FRAMES = 300  # 5 minutos de fotogramas en RAM (~4 MB de memoria)
JPEG_BUFFER = collections.deque(maxlen=MAX_RAM_FRAMES)
BUFFER_LOCK = threading.Lock()

LATEST_WEBCAM_FRAME = None
WEBCAM_LOCK = threading.Lock()

def workload_monitor_thread():
    """Detecta juegos o simuladores en ejecución para suspender la grabación en segundo plano."""
    global IS_OPTIMIZED_MODE, CURRENT_WORKLOAD_NAME
    while True:
        try:
            found = None
            for proc in psutil.process_iter(['name']):
                try:
                    pname = (proc.info['name'] or '').lower()
                    if pname in CRITICAL_WORKLOAD_PROCESSES:
                        found = pname
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            IS_OPTIMIZED_MODE = bool(found)
            CURRENT_WORKLOAD_NAME = found
        except Exception:
            pass
        time.sleep(4)

threading.Thread(target=workload_monitor_thread, daemon=True).start()

def get_live_screen_image():
    """Captura de pantalla acelerada por hardware nativo GDI en Windows."""
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    kernel32 = ctypes.windll.kernel32

    kernel32.SetThreadExecutionState(0x80000000 | 0x00000001 | 0x00000002)

    hwnd = user32.GetForegroundWindow()
    hdesktop = user32.OpenInputDesktop(0, False, 0x0001)
    
    if not hdesktop or hwnd == 0:
        if hdesktop: user32.CloseDesktop(hdesktop)
        return None
    user32.CloseDesktop(hdesktop)

    try:
        w = user32.GetSystemMetrics(0)
        h = user32.GetSystemMetrics(1)
        if w <= 0 or h <= 0: return None

        desktop_dc = user32.GetDC(0)
        img_dc = gdi32.CreateCompatibleDC(desktop_dc)
        mem_bitmap = gdi32.CreateCompatibleBitmap(desktop_dc, w, h)
        gdi32.SelectObject(img_dc, mem_bitmap)
        
        gdi32.BitBlt(img_dc, 0, 0, w, h, desktop_dc, 0, 0, 0x00CC0020 | 0x40000000)
        
        class BITMAPINFOHEADER(ctypes.Structure):
            _fields_ = [
                ('biSize', ctypes.c_uint32),
                ('biWidth', ctypes.c_int32),
                ('biHeight', ctypes.c_int32),
                ('biPlanes', ctypes.c_uint16),
                ('biBitCount', ctypes.c_uint16),
                ('biCompression', ctypes.c_uint32),
                ('biSizeImage', ctypes.c_uint32),
                ('biXPelsPerMeter', ctypes.c_int32),
                ('biYPelsPerMeter', ctypes.c_int32),
                ('biClrUsed', ctypes.c_uint32),
                ('biClrImportant', ctypes.c_uint32)
            ]
        
        bmi = BITMAPINFOHEADER()
        bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bmi.biWidth = w
        bmi.biHeight = -h
        bmi.biPlanes = 1
        bmi.biBitCount = 32
        bmi.biCompression = 0
        
        buffer = ctypes.create_string_buffer(w * h * 4)
        gdi32.GetDIBits(img_dc, mem_bitmap, 0, h, buffer, ctypes.byref(bmi), 0)
        
        gdi32.DeleteObject(mem_bitmap)
        gdi32.DeleteDC(img_dc)
        user32.ReleaseDC(0, desktop_dc)
        
        img = Image.frombuffer('RGBA', (w, h), buffer, 'raw', 'BGRA', 0, 1).convert('RGB')
        arr = np.array(img)
        if arr.mean() < 0.5:
            return None
        return img
    except Exception:
        return None

def get_shared_webcam_frame():
    """Retorna una copia segura del último fotograma de la webcam."""
    global LATEST_WEBCAM_FRAME
    with WEBCAM_LOCK:
        if LATEST_WEBCAM_FRAME is not None:
            return LATEST_WEBCAM_FRAME.copy()
    return None

def generate_locked_screen_placeholder():
    """Genera una imagen informativa cuando la pantalla se encuentra bloqueada."""
    base = Image.new("RGB", (1280, 720), color=(10, 14, 23))
    d = ImageDraw.Draw(base)
    
    d.rectangle([(80, 180), (1200, 540)], fill=(17, 24, 39), outline=(56, 189, 248), width=2)
    d.rectangle([(80, 180), (1200, 245)], fill=(22, 32, 50))
    d.text((110, 205), "OPENSENTINEL // ESTACIÓN EN MODO SEGURO (SESIÓN BLOQUEADA)", fill=(56, 189, 248))
    
    d.text((110, 280), "• Estado de Windows: Sesión protegida con contraseña", fill=(248, 250, 252))
    d.text((110, 325), "• Seguridad de Pantalla: El kernel protege el escritorio privado", fill=(148, 163, 184))
    d.text((110, 370), "• Sensor Óptico (Webcam): Vigilancia activa en segundo plano", fill=(16, 185, 129))
    d.text((110, 415), "• Para reactivar: Pulsa 'Despertar Pantalla' en la pestaña Seguridad", fill=(245, 158, 11))
    
    ts = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    d.text((110, 480), f"Timestamp Forense: {ts} // Nodo Protegido", fill=(100, 116, 139))
    return base

def build_composite_evidence_frame(screen_img, webcam_frame):
    """Construye un fotograma forense con Pantalla + Sensor de Webcam en PiP + Timestamp."""
    import cv2
    base = np.zeros((720, 1280, 3), dtype=np.uint8)
    base[:] = (10, 14, 23)

    if screen_img is not None:
        try:
            screen_np = np.array(screen_img)
            screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR)
            base = cv2.resize(screen_bgr, (1280, 720))
        except Exception:
            pass
    else:
        locked_img = generate_locked_screen_placeholder()
        locked_np = np.array(locked_img)
        base = cv2.cvtColor(locked_np, cv2.COLOR_RGB2BGR)

    if webcam_frame is not None:
        try:
            cam_resized = cv2.resize(webcam_frame, (320, 180))
            cv2.rectangle(base, (1280 - 332, 18), (1280 - 8, 202), (56, 189, 248), 2)
            base[20:200, 1280 - 330:1280 - 10] = cam_resized
            cv2.putText(base, "SENSOR OPTICO [VIVO]", (1280 - 324, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 128), 1)
        except Exception:
            pass

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    cv2.rectangle(base, (10, 10), (480, 42), (0, 0, 0), -1)
    cv2.rectangle(base, (10, 10), (480, 42), (56, 189, 248), 1)
    cv2.putText(base, f"REGISTRO FORENSE // {ts}", (20, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 1)

    return base

def continuous_recorder_loop(enable_webcam=True, enable_screenshot=True):
    """Hilo continuo de grabación forense en memoria RAM."""
    global LATEST_WEBCAM_FRAME
    import cv2
    cap = None

    while True:
        if IS_OPTIMIZED_MODE or not enable_webcam:
            if cap is not None:
                try: cap.release()
                except Exception: pass
                cap = None
            time.sleep(2)
            continue

        start_t = time.time()
        screen_img = get_live_screen_image() if enable_screenshot else None

        webcam_frame = None
        if cap is None or not cap.isOpened():
            for idx in (0, 1, 2):
                c = cv2.VideoCapture(idx)
                if c.isOpened():
                    cap = c; break
        
        if cap is not None and cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                webcam_frame = frame
                with WEBCAM_LOCK:
                    LATEST_WEBCAM_FRAME = frame.copy()

        composite = build_composite_evidence_frame(screen_img, webcam_frame)
        success, jpeg_bytes = cv2.imencode(".jpg", composite, [cv2.IMWRITE_JPEG_QUALITY, 60])
        if success:
            with BUFFER_LOCK:
                JPEG_BUFFER.append(jpeg_bytes.tobytes())

        elapsed = time.time() - start_t
        time.sleep(max(0.05, 1.0 - elapsed))

def start_surveillance_threads(enable_webcam=True, enable_screenshot=True):
    """Inicia los hilos en segundo plano para la vigilancia."""
    t = threading.Thread(target=continuous_recorder_loop, args=(enable_webcam, enable_screenshot), daemon=True)
    t.start()
    return t

def export_in_ram_video(clips_dir: Path) -> dict:
    """Compila los fotogramas acumulados en RAM en un archivo MP4 descargable."""
    import cv2
    with BUFFER_LOCK:
        jpeg_list = list(JPEG_BUFFER)
    
    if not jpeg_list or len(jpeg_list) < 2:
        return {"error": "Búfer de vídeo insuficiente. Inicializando grabación..."}

    for old in clips_dir.glob("*.mp4"):
        try: old.unlink()
        except Exception: pass

    filename = "evidencia_actual.mp4"
    out_path = clips_dir / filename
    
    first_frame = cv2.imdecode(np.frombuffer(jpeg_list[0], np.uint8), cv2.IMREAD_COLOR)
    h, w, _ = first_frame.shape
    
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(out_path), fourcc, 10.0, (w, h))
    
    for raw_bytes in jpeg_list:
        frame = cv2.imdecode(np.frombuffer(raw_bytes, np.uint8), cv2.IMREAD_COLOR)
        if frame is not None:
            writer.write(frame)
    writer.release()
    
    dur_secs = len(jpeg_list)
    dur_str = f"{dur_secs // 60}m {dur_secs % 60}s"
    
    return {
        "url": f"/clips/{filename}",
        "filename": f"forensic_evidence_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
        "duration": dur_str
    }
