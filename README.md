# OpenSentinel

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6.svg?style=flat-square&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Co-Authored with Claude](https://img.shields.io/badge/Co--Authored%20with-Claude%20(Anthropic)-D97706.svg?style=flat-square&logo=anthropic&logoColor=white)](https://anthropic.com)
[![Architecture: Zero-Cloud](https://img.shields.io/badge/Architecture-100%25%20Zero--Cloud-059669.svg?style=flat-square)](#privacy-and-security-protocols)
[![Forensics: RAM Buffer](https://img.shields.io/badge/Forensics-0%20MB%20Disk%20Wear-3B82F6.svg?style=flat-square)](#key-features)
[![Panic Lockdown](https://img.shields.io/badge/DEFCON--1-1ms%20Lockdown-EF4444.svg?style=flat-square)](#key-features)
[![Discord Alerts](https://img.shields.io/badge/Alerts-Discord-5865F2.svg?style=flat-square&logo=discord&logoColor=white)](https://discord.com)
[![Telegram Alerts](https://img.shields.io/badge/Alerts-Telegram-26A5E4.svg?style=flat-square&logo=telegram&logoColor=white)](https://telegram.org)
[![WhatsApp Alerts](https://img.shields.io/badge/Alerts-WhatsApp-25D366.svg?style=flat-square&logo=whatsapp&logoColor=white)](https://whatsapp.com)

**Lightweight, zero-cloud security sentinel, in-RAM forensic recorder, and remote PC telemetry console tailored for Windows workstations.**

[Quick Start](#quick-start-step-by-step-installation) · [Channel Setup](#channel-configuration-guide) · [Key Features](#key-features) · [Architecture](#architecture) · [REST API](#rest-api-reference) · [FAQ](#faq--troubleshooting)

**English** · [Español](README.es.md)

</div>

---

## Overview

**OpenSentinel** is an autonomous cybersecurity sentinel and real-time telemetry console designed for Windows workstations. It operates under a strict **zero-cloud dependency** architecture:

1. **Anti-Spam Physical Boot Watchdog:** Monitors Windows boot events and dispatches **strictly one executive notification per physical boot session** across configured channels (Discord, Telegram, WhatsApp), completely eliminating notification spam loops during service restarts.
2. **In-RAM Dual Forensic Recorder:** Continuously maintains a **5-minute rolling ring buffer** (native GDI screen capture + shared optical webcam PiP) stored **100% in volatile RAM** (0 MB wear on SSDs/HDDs).
3. **DEFCON-1 Panic Lockdown Protocol:** Executes an emergency response in **1 millisecond**: stealth webcam evidence capture to RAM, hardware audio muting, and immediate Windows session lock.
4. **Glassmorphic SPA Remote Dashboard:** Low-latency dark control console accessible locally over LAN or end-to-end encrypted from anywhere via **Tailscale P2P**.
5. **Multi-Language Architecture (i18n):** Native bilingual support (English & Spanish) across the web dashboard, CLI configuration wizard, alert notifications, and REST API.

---

## Key Features

* **Intelligent Anti-Spam Boot Lock:** Compares Windows kernel boot timestamps (`boot_session.json`) to guarantee **only 1 alert per physical machine boot**, eliminating repetitive notification floods.
* **Multi-Channel Alert Broadcast:** Simultaneous native broadcasting to **Discord Webhooks**, **Telegram Bot API**, and **WhatsApp** (CallMeBot or custom webhook).
* **Multi-Language (i18n):** Instant on-the-fly language switching (English / Español) across Web UI, CLI setup wizard, and alert notifications.
* **Glassmorphic SPA Console:** Modern dark dashboard with animated gauges (CPU load, RAM memory, dynamic multi-drive detection `C:`, `D:`, `E:`), active window tracking, and process termination controls.
* **In-RAM Rolling Forensic Buffer:** 5-minute continuous screen + webcam video buffer stored entirely in RAM. Compiles to MP4 video with a single click.
* **DEFCON-1 Panic Lockdown:** Single-click panic trigger: silent optical snapshot, instant speaker silencing, and 1ms workstation lock.
* **Workload-Aware Zero-Overhead:** Automatically detects gaming and heavy compute workloads (simulators, rendering software, 3D suites) to pause background capture and ensure **0.0% residual performance impact**.
* **Secure P2P Networking:** Zero router port forwarding required. Direct authenticated access via Tailscale or integrated reverse proxy.

---

## Architecture

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

## Quick Start: Step-by-Step Installation

### Step 1: Prerequisites
* **Operating System:** Windows 10 or Windows 11 (64-bit).
* **Python:** Version **3.10 or higher**. Ensure the **"Add Python to PATH"** checkbox is selected during Python installation.
* **Git** (Optional, to clone the repository).

### Step 2: Download or Clone
Open a terminal (PowerShell or CMD) and run:
```bash
git clone https://github.com/atrumin16/open-sentinel.git
cd open-sentinel
```
*(Or download the repository ZIP file from GitHub and extract it to your preferred folder).*

### Step 3: 1-Click Installation
Double-click **`scripts/install.bat`** (or run `python main.py --setup` in terminal):
1. **Dependency Verification:** Silently installs required packages (`requirements.txt`).
2. **Language Selection:** Prompts for your preferred language (English or Spanish).
3. **Telemetry & Setup:** Displays your workstation hardware specs and guides you to configure your server name and alert channels.
4. **Live Connectivity Test:** Dispatches test pings to your configured notification channels to verify connectivity before saving.
5. **Silent Windows Autostart:** Registers a background shortcut in the Windows Startup folder via `run_hidden.vbs` (**0% residual CPU usage** with no popup command prompt windows).

---

## Channel Configuration Guide

The interactive wizard `scripts/setup.bat` (or the Web Dashboard Settings tab) allows activating any combination of channels:

### 1. Discord Webhooks (Recommended)
1. In your Discord server, open channel settings: **Channel > Edit Channel (gear icon) > Integrations**.
2. Click **"Create Webhook"** (or "View Webhooks").
3. Name your webhook (e.g. `OpenSentinel`) and click **"Copy Webhook URL"**.
4. Paste the URL into the installer (`https://discord.com/api/webhooks/...`).

### 2. Telegram Bot API
1. Open Telegram and search for **[@BotFather](https://t.me/botfather)**.
2. Send `/newbot`, assign a name and username to your bot.
3. Copy the provided **HTTP API Token** (e.g. `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`).
4. To obtain your numerical Chat ID, open **[@userinfobot](https://t.me/userinfobot)** and press `/start`.
5. Paste the Token and Chat ID into the installer.

### 3. WhatsApp (via CallMeBot)
1. Add **`+34 644 10 55 84`** to your phone contacts (or click [this direct link](https://wa.me/34644105584?text=I%20allow%20callmebot%20to%20send%20me%20messages)).
2. Send this exact message via WhatsApp:
   ```text
   I allow callmebot to send me messages
   ```
3. You will receive an automated reply with your personal **API Key** in seconds.
4. Enter your phone number with international country code (e.g. `+34600112233`) and your API Key.

### 4. Secure Remote Access (Tailscale P2P)
To monitor and control your workstation from your smartphone without opening router ports:
1. Install **[Tailscale](https://tailscale.com/)** on your PC and your phone.
2. Sign in with the same account on both devices.
3. OpenSentinel automatically detects your Tailscale IP (`100.x.y.z`).
4. Access your dashboard securely from anywhere: `http://<TAILSCALE_IP>:8888`.

---

## Background Service Management

The `scripts/` directory includes quick operational utilities:

| Script | Action |
| :--- | :--- |
| **`scripts/install.bat`** | Complete installer: dependencies, interactive setup wizard, and Windows startup registration. |
| **`scripts/start.bat`** | Launches OpenSentinel silently in the background. |
| **`scripts/stop.bat`** | Instantly terminates all active OpenSentinel processes. |
| **`scripts/setup.bat`** | Opens the channel reconfiguration wizard at any time. |
| **`scripts/uninstall.bat`** | Cleanly removes the background autostart shortcut and stops active instances. |

---

## Privacy and Security Protocols

* **Default IP Filtering:** The web server strictly accepts connections originating from private subnets (`192.168.*`, `10.*`, `172.*`, `127.0.0.1`) and the Tailscale P2P mesh (`100.*`). Public internet requests are rejected automatically with HTTP 403.
* **Zero-Wear Forensics:** Rolling buffer frames are maintained exclusively in volatile RAM. Zero bytes are written to disk until the user explicitly requests an export.
* **Credential Hygiene:** `config.json` and `boot_session.json` are excluded from version control via `.gitignore`.

---

## REST API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/stats` | `GET` | Real-time telemetry: CPU, RAM, dynamic multi-drives, uptime, active window. |
| `/api/processes` | `GET` | Top processes sorted by RAM consumption. |
| `/api/processes/kill?pid=X` | `POST` | Safely terminates a process by PID. |
| `/api/screenshot` | `GET` | Real-time native GDI screen capture. |
| `/api/webcam` | `GET` | Live optical webcam frame. |
| `/api/generate_clip` | `POST` | Compiles the 5-minute RAM buffer into a downloadable MP4 video. |
| `/api/defcon/panic` | `POST` | Triggers DEFCON-1: silent photo grab, hardware audio mute, 1ms workstation lock. |
| `/api/power/lock` | `POST` | Locks the current Windows user session. |
| `/api/power/sleep` | `POST` | Places the workstation into S3 sleep state. |
| `/api/power/shutdown` | `POST` | Schedules clean workstation shutdown (10-second safety window). |
| `/api/power/reboot` | `POST` | Schedules clean workstation reboot (10-second safety window). |
| `/api/power/cancel` | `POST` | Aborts a scheduled shutdown or reboot. |
| `/api/power/wake_screen` | `POST` | Wakes monitors and desktop window manager (DWM). |
| `/api/config` | `GET/POST` | Reads or updates settings on the fly (including language preference). |
| `/api/i18n` | `GET` | Fetches translation dictionary for the requested or all languages. |
| `/api/test_notification` | `POST` | Dispatches a live test alert to `discord`, `telegram`, or `whatsapp`. |

---

## FAQ & Troubleshooting

<details>
<summary><b>1. 'python' is not recognized as an internal or external command</b></summary>
Re-run the Python installer from <a href="https://www.python.org/downloads/">python.org</a> and make sure to check the box <b>"Add Python to PATH"</b> on the very first screen. Restart your terminal afterwards.
</details>

<details>
<summary><b>2. Windows Defender Firewall prompt appears</b></summary>
Click <b>"Allow access"</b> ensuring the <i>"Private networks"</i> checkbox is enabled. OpenSentinel needs to bind port 8888 so you can access the dashboard over LAN or Tailscale.
</details>

<details>
<summary><b>3. Webcam feed displays a black screen</b></summary>
In Windows 10/11, open <b>Settings > Privacy & Security > Camera</b> and ensure <i>"Let desktop apps access your camera"</i> is turned ON.
</details>

<details>
<summary><b>4. How do I verify OpenSentinel is running in the background?</b></summary>
Open your browser and navigate to <a href="http://127.0.0.1:8888">http://127.0.0.1:8888</a>. If the console loads, the sentinel is actively protecting the workstation. You can also inspect Task Manager for the <code>pythonw.exe</code> process.
</details>

---

## Engineering Credits & Co-Authorship

OpenSentinel was engineered, built, and fortified with high-reliability zero-trust architecture by:
* **Alberto Trujillo Mingorance** ([@atrumin16](https://github.com/atrumin16)) — Systems architecture, low-level hardware telemetry, in-RAM forensic engine, and DEFCON-1 panic protocol design.
* **Claude** ([Anthropic](https://anthropic.com)) — Co-authorship in zero-trust sentinel protocol design, asynchronous alert pipelines, and codebase hardening.

---

## License

Distributed under the **MIT** License. See [`LICENSE`](LICENSE) for full details.
