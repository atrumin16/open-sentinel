# 🛡️ OpenSentinel

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6.svg?logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Discord Alerts](https://img.shields.io/badge/Alerts-Discord-5865F2.svg?logo=discord&logoColor=white)](https://discord.com)
[![Telegram Alerts](https://img.shields.io/badge/Alerts-Telegram-26A5E4.svg?logo=telegram&logoColor=white)](https://telegram.org)
[![WhatsApp Alerts](https://img.shields.io/badge/Alerts-WhatsApp-25D366.svg?logo=whatsapp&logoColor=white)](https://whatsapp.com)

**Open-source, self-hosted PC telemetry, multi-channel boot sentinel, and remote forensic security console.**

[Features](#-key-features) • [Quick Start](#-quick-start-2-clicks) • [Architecture](#-architecture) • [Notification Channels](#-multi-channel-alerts) • [REST API](#-rest-api-reference)

</div>

---

## 🌟 Overview

**OpenSentinel** is a lightweight, zero-latency, self-hosted sentinel system designed for Windows workstations. It automatically monitors system boot events, broadcasts clean executive alerts across **Discord, Telegram, and WhatsApp**, and provides a cyber-grade **Glassmorphic Single-Page Application (SPA)** dashboard for real-time telemetry, remote session management, and in-RAM forensic evidence capture.

---

## 🚀 Key Features

* **🛑 Zero-Spam Smart Boot Sentinel:** Tracks kernel boot timestamps (`boot_session.json`) to guarantee **exactly 1 alert per power-on session**, blocking repetitive notifications even across script restarts.
* **📱 Multi-Channel Broadcast:** Configurable per-user alerting via **Discord Webhooks**, **Telegram Bot API**, and **WhatsApp** (CallMeBot or custom webhooks).
* **💎 Glassmorphic SPA Dashboard:** Sleek, dark-mode real-time console with animated gauges (CPU, RAM, multi-drive storage `C:`, `D:`, `E:`), active window tracking, and mobile responsiveness via Tailscale P2P.
* **👁️ In-RAM Forensic Recorder:** Native GDI hardware screen capture, live optical webcam streaming, and a rolling 5-minute RAM video buffer (Dual Screen + PiP Webcam) with **0 MB continuous disk footprint**.
* **🚨 DEFCON-1 Panic Protocol:** 1-click emergency lockdown: captures a silent webcam photo into RAM, mutes hardware audio, and locks Windows workstation in **1 millisecond**.
* **🎮 Workload Optimization:** Automatically pauses forensic recording when gaming or heavy simulation processes (iRacing, Assetto Corsa, Blender, etc.) are detected, ensuring **0.0% residual load**.
* **⚡ 2-Click Turnkey Deployment:** 100% dynamic hardware and network discovery. Works out of the box on any computer without hardcoding paths or IPs.

---

## 🏗️ Architecture

```
                                  +-----------------------+
                                  |   Windows Boot Event  |
                                  +-----------+-----------+
                                              |
                                              v
+-----------------------------------------------------------------------------------+
|                               OPENSENTINEL CORE                                   |
|                                                                                   |
|  [ Hardware Telemetry ]       [ In-RAM Dual Recorder ]      [ DEFCON-1 Lockdown ] |
|  - CPU / GPU / RAM            - Native GDI Screen           - Silent Webcam Grab  |
|  - Multi-Drive Storage        - Shared Webcam Stream        - 1ms Session Lock    |
|  - Active Window Tracker      - 5-Min Rolling RAM Buffer    - Hardware Audio Mute |
+-----------------------------------------+-----------------------------------------+
                                          |
                      +-------------------+-------------------+
                      |                                       |
                      v                                       v
        +----------------------------+          +---------------------------+
        |   Multi-Channel Alerter    |          |    Executive Web Server   |
        |   (Anti-Spam Session Lock) |          |    (Tailscale & LAN SPA)  |
        +--------------+-------------+          +-------------+-------------+
                       |                                      |
         +-------------+-------------+                        |
         |             |             |                        v
         v             v             v              +--------------------+
    [ Discord ]   [ Telegram ]  [ WhatsApp ]        |   Remote Console   |
     Webhooks       Bot API      CallMeBot          | (Desktop / Mobile) |
                                                    +--------------------+
```

---

## ⚡ Quick Start (Instalación en 2 Clics)

### 1. Clonar el repositorio
```bash
git clone https://github.com/atrumin16/open-sentinel.git
cd open-sentinel
```

### 2. Ejecutar el Instalador Interactivo
Haz doble clic en **`scripts/install.bat`** (o ejecuta `python main.py --setup`):
* Instala automáticamente las dependencias necesarias (`requirements.txt`).
* Inicia un **asistente interactivo en consola** que detecta tu hardware e IP automáticamente y te guía para configurar tu nombre de servidor, Webhook de Discord, Telegram o WhatsApp.
* Permite enviar un mensaje de prueba en tiempo real para verificar la conexión.
* **NUEVO:** Ofrece la configuración automática de una Red Segura (Proxy Inverso Caddy + Tailscale) para acceder a través de tu dominio personalizado (ej: `dash.midominio.com` o `alertas.local`).
* Registra el inicio automático silencioso en segundo plano de Windows (0% CPU residual).
* Inicia el servidor OpenSentinel y abre el panel de control.

Para reconfigurar en cualquier momento, ejecuta `scripts/setup.bat` o `python main.py --setup`.
Para configurar o actualizar tu Proxy Inverso (Caddy/Tailscale) manualmente, ejecuta `scripts/setup_network.ps1`.

---

## 🌐 Access Points

| Channel | URL | Purpose |
| :--- | :--- | :--- |
| **Remote Access (Tailscale P2P)** | `http://<TAILSCALE_IP>:8888` | Encrypted, direct mobile/remote control |
| **Local Access (LAN)** | `http://<LOCAL_LAN_IP>:8888` | Home/Office network access |
| **Local Host** | `http://127.0.0.1:8888` | On-machine console access |

---

## 📱 Multi-Channel Alerts

Configure your notification channels in `config.json` or directly from the **Ajustes** tab in the web console:

```json
{
  "SERVER_NAME": "OpenSentinel",
  "PORT": 8888,
  "AUTO_ALERT_ON_BOOT": true,

  "DISCORD_ENABLED": true,
  "DISCORD_WEBHOOK_URL": "https://discord.com/api/webhooks/...",
  "DISCORD_THREAD_ID": "",

  "TELEGRAM_ENABLED": true,
  "TELEGRAM_BOT_TOKEN": "123456789:ABCdef...",
  "TELEGRAM_CHAT_ID": "123456789",

  "WHATSAPP_ENABLED": true,
  "WHATSAPP_PROVIDER": "callmebot",
  "WHATSAPP_PHONE": "+34600000000",
  "WHATSAPP_API_KEY": "YOUR_API_KEY"
}
```

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/stats` | `GET` | Real-time system telemetry (CPU, RAM, Disks, Window). |
| `/api/processes` | `GET` | Top processes sorted by RAM memory usage. |
| `/api/processes/kill?pid=X` | `POST` | Safely terminates a process by PID. |
| `/api/screenshot` | `GET` | Native GDI live screenshot. |
| `/api/webcam` | `GET` | Live webcam optical sensor snapshot. |
| `/api/generate_clip` | `POST` | Compiles rolling RAM buffer into an MP4 video clip. |
| `/api/defcon/panic` | `POST` | Triggers DEFCON-1 silent capture & 1ms lockdown. |
| `/api/power/lock` | `POST` | Locks Windows workstation session. |
| `/api/power/sleep` | `POST` | Puts system into S3 sleep mode. |
| `/api/power/shutdown` | `POST` | Schedules safe 10-second shutdown. |
| `/api/power/reboot` | `POST` | Schedules safe 10-second reboot. |
| `/api/power/cancel` | `POST` | Aborts pending reboot or shutdown. |
| `/api/power/wake_screen` | `POST` | Turns on displays and wakes DWM compositor. |
| `/api/config` | `GET/POST` | Reads or updates configuration in runtime. |
| `/api/test_notification` | `POST` | Sends test pings to `discord`, `telegram`, or `whatsapp`. |

---

## 🔒 Security & Privacy

* **IP Filtering:** Restricts access strictly to local private subnets (`192.168.*`, `10.*`, `172.*`, `127.0.0.1`) and Tailscale P2P mesh (`100.*`).
* **Zero-Disk Forensics:** Live video buffers remain 100% in RAM memory until explicitly exported.
* **Credential Hygiene:** Sensitive tokens and session files are excluded from Git via `.gitignore`.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.

1. Fork the repository
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

Developed by [Alberto](https://github.com/atrumin16) and OpenSentinel Contributors.
