# OpenSentinel

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6.svg?style=flat-square&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Co-Authored with Claude](https://img.shields.io/badge/Co--Authored%20with-Claude%20(Anthropic)-D97706.svg?style=flat-square&logo=anthropic&logoColor=white)](https://anthropic.com)
[![Architecture: Zero-Cloud](https://img.shields.io/badge/Architecture-100%25%20Zero--Cloud-059669.svg?style=flat-square)](#privacidad-y-protocolos-de-seguridad)
[![Forensics: RAM Buffer](https://img.shields.io/badge/Forensics-0%20MB%20Disk%20Wear-3B82F6.svg?style=flat-square)](#características-principales)
[![Panic Lockdown](https://img.shields.io/badge/DEFCON--1-1ms%20Lockdown-EF4444.svg?style=flat-square)](#características-principales)
[![Discord Alerts](https://img.shields.io/badge/Alerts-Discord-5865F2.svg?style=flat-square&logo=discord&logoColor=white)](https://discord.com)
[![Telegram Alerts](https://img.shields.io/badge/Alerts-Telegram-26A5E4.svg?style=flat-square&logo=telegram&logoColor=white)](https://telegram.org)
[![WhatsApp Alerts](https://img.shields.io/badge/Alerts-WhatsApp-25D366.svg?style=flat-square&logo=whatsapp&logoColor=white)](https://whatsapp.com)

**Lightweight, zero-cloud security sentinel, in-RAM forensic recorder, and remote PC telemetry console tailored for Windows workstations.**

[Quick Start](#quick-start-instalación-paso-a-paso) · [Guía de Canales](#guía-de-configuración-de-canales) · [Características](#características-principales) · [Arquitectura](#arquitectura) · [API REST](#referencia-de-api-rest) · [FAQ](#faq--solución-de-problemas)

[English](README.md) · **Español**

</div>

---

## Visión General

**OpenSentinel** es una solución centinela autónoma de ciberseguridad y telemetría en tiempo real para estaciones de trabajo Windows. Opera con un principio estricto de **cero dependencia en la nube**:
1. Supervisa los arranques físicos de Windows y emite **estrictamente una sola alerta ejecutiva por sesión de encendido** a tus canales de mensajería (Discord, Telegram y WhatsApp), sin bucles de spam al reiniciar servicios.
2. Mantiene una **cámara forense continua de 5 minutos** (captura de pantalla GDI + webcam PiP) almacenada **100% en memoria RAM** (0 MB de desgaste en SSD o disco duro).
3. Dispone de un **protocolo de pánico DEFCON-1**: captura silenciosa de foto webcam en RAM, silenciado instantáneo de audio hardware y bloqueo inmediato de la sesión de Windows en **1 milisegundo**.
4. Ofrece un **panel web glassmórfico de alta fidelidad** accesible localmente en red LAN o cifrado punto a punto en cualquier lugar mediante **Tailscale P2P**.

---

## Características Principales

* **Centinela Inteligente Anti-Spam:** Compara marcas temporales de arranque del kernel Windows (`boot_session.json`) para garantizar que **solo se envía 1 alerta por encendido físico**, evitando bucles de alertas si el script o servicio se reinicia.
* **Difusión Multi-Canal:** Soporte nativo y simultáneo para **Webhooks de Discord**, **Bots de Telegram** y **WhatsApp** (vía CallMeBot o webhook propio).
* **Consola Glassmórfica SPA:** Dashboard oscuro de baja latencia con medidores animados (CPU, RAM, detección dinámica de discos `C:`, `D:`, `E:`), ventana activa y control total de procesos.
* **Búfer Forense en RAM (Rolling Ring Buffer):** Grabación continua de pantalla completa y webcam en anillo circular de memoria RAM. Exportable a vídeo MP4 con un solo clic ante cualquier incidente.
* **Protocolo de Pánico DEFCON-1:** Gatillo de emergencia de 1 clic: foto sigilosa de la webcam, silenciado de altavoces y bloqueo instantáneo de la sesión de Windows.
* **Conciencia de Carga de Trabajo (0% Overhead):** Detecta automáticamente cuándo se ejecutan juegos o tareas pesadas (Blender, simuladores, renderizadores) para pausar la grabación en RAM y mantener un **0.0% de impacto en el rendimiento**.
* **Red Segura y P2P:** Sin abrir puertos en el router. Acceso seguro garantizado con Tailscale o proxy inverso Caddy integrado.

---

## Arquitectura

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

## Quick Start: Instalación Paso a Paso

### Paso 1: Requisitos Previos
* **Sistema Operativo:** Windows 10 o Windows 11 (64 bits).
* **Python:** Versión **3.10 o superior**. Asegúrate de marcar la casilla **"Add Python to PATH"** durante la instalación de Python.
* **Git** (Opcional, para clonar el repositorio).

### Paso 2: Descargar o Clonar
Abre una terminal (PowerShell o CMD) y ejecuta:
```bash
git clone https://github.com/atrumin16/open-sentinel.git
cd open-sentinel
```
*(O descarga el repositorio en ZIP desde GitHub y descomprímelo en tu carpeta personal).*

### Paso 3: Instalación en 1 Clic
Haz **doble clic en `scripts/install.bat`** (o ejecuta en consola `python main.py --setup`):
1. **Verificación Automática:** Instala dependencias (`requirements.txt`) silenciosamente.
2. **Asistente Guiado:** Muestra la telemetría de tu PC y te guía para configurar tu nombre de equipo y tus canales de alerta.
3. **Prueba en Vivo:** Envía un ping de prueba a tus canales configurados para verificar la conectividad antes de guardar.
4. **Inicio Automático Silencioso:** Configura un acceso directo en el arranque de Windows mediante `run_hidden.vbs` para ejecutarse en segundo plano con **0% de consumo de CPU** y sin ventanas negras molestas.

---

## Guía de Configuración de Canales

El asistente `scripts/setup.bat` (o el panel de ajustes de la web) te permite activar los canales que desees:

### 1. Discord Webhooks (Recomendado)
1. En tu servidor de Discord, entra en los ajustes de cualquier canal de texto: **Canal > Editar Canal (rueda dentada) > Integraciones**.
2. Haz clic en **"Crear Webhook"** (o "Ver Webhooks").
3. Asigna el nombre que quieras (ej: `OpenSentinel`) y haz clic en **"Copiar URL de Webhook"**.
4. Pega la URL en el instalador (`https://discord.com/api/webhooks/...`).

### 2. Telegram Bot API
1. Abre Telegram y busca a **[@BotFather](https://t.me/botfather)**.
2. Envía el comando `/newbot`, asigna un nombre y un usuario a tu bot.
3. Copia el **HTTP API Token** proporcionado (ej: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`).
4. Para saber tu ID de usuario, abre **[@userinfobot](https://t.me/userinfobot)** y dale a `/start`. Te devolverá tu **Id** numérico.
5. Pega el Token y tu Chat ID en el instalador.

### 3. WhatsApp (vía CallMeBot)
1. Añade el contacto **`+34 644 10 55 84`** a tu agenda de WhatsApp (o haz clic en [este enlace directo](https://wa.me/34644105584?text=I%20allow%20callmebot%20to%20send%20me%20messages)).
2. Envíale este mensaje exacto:
   ```text
   I allow callmebot to send me messages
   ```
3. Recibirás un mensaje automático con tu **API Key** personal en segundos.
4. En el asistente, introduce tu número en formato internacional (ej: `+34600112233`) y tu API Key.

### 4. Acceso Remoto Seguro (Tailscale P2P)
Si deseas controlar tu PC desde tu móvil o fuera de casa sin abrir puertos en tu router:
1. Instala **[Tailscale](https://tailscale.com/)** en tu PC y en tu teléfono móvil.
2. Inicia sesión con la misma cuenta en ambos dispositivos.
3. OpenSentinel detectará automáticamente tu IP de Tailscale (`100.x.y.z`).
4. Accede desde tu móvil a: `http://<TU_IP_TAILSCALE>:8888`.

---

## Gestión del Centinela en Segundo Plano

En la carpeta `scripts/` dispones de herramientas rápidas:

| Script | Acción |
| :--- | :--- |
| **`scripts/install.bat`** | Instalador completo, dependencias, asistente y registro en inicio de Windows. |
| **`scripts/start.bat`** | Inicia OpenSentinel silenciosamente en segundo plano. |
| **`scripts/stop.bat`** | Detiene todos los procesos activos de OpenSentinel al instante. |
| **`scripts/setup.bat`** | Abre el asistente de reconfiguración de canales en cualquier momento. |
| **`scripts/uninstall.bat`** | Elimina el arranque automático silencioso del sistema de forma limpia. |

---

## Privacidad y Protocolos de Seguridad

* **Filtrado de IPs por Defecto:** El servidor web solo acepta conexiones procedentes de subredes privadas locales (`192.168.*`, `10.*`, `172.*`, `127.0.0.1`) y de la malla P2P de Tailscale (`100.*`). Peticiones públicas externas son rechazadas automáticamente.
* **Forense Cero-Desgaste:** Las capturas en búfer continuo se mantienen en memoria RAM volátil. No se escribe ni un solo byte en disco hasta que el usuario pulsa explícitamente "Generar Clip Forense".
* **Higiene de Credenciales:** `config.json` y `boot_session.json` están excluidos del control de versiones mediante `.gitignore`.

---

## Referencia de API REST

| Endpoint | Método | Descripción |
| :--- | :--- | :--- |
| `/api/stats` | `GET` | Telemetría en tiempo real: CPU, RAM, discos dinámicos, ventana activa. |
| `/api/processes` | `GET` | Lista de procesos principales ordenados por consumo de RAM. |
| `/api/processes/kill?pid=X` | `POST` | Termina un proceso de forma segura según su PID. |
| `/api/screenshot` | `GET` | Captura de pantalla nativa GDI en tiempo real. |
| `/api/webcam` | `GET` | Fotograma óptico de la cámara web. |
| `/api/generate_clip` | `POST` | Compila el búfer de RAM de 5 minutos en un clip MP4. |
| `/api/defcon/panic` | `POST` | Ejecuta el protocolo DEFCON-1: foto sigilosa, silenciado de audio y bloqueo. |
| `/api/power/lock` | `POST` | Bloquea la sesión de usuario de Windows. |
| `/api/power/sleep` | `POST` | Pone la estación de trabajo en suspensión S3. |
| `/api/power/shutdown` | `POST` | Programa apagado seguro con margen de 10 segundos. |
| `/api/power/reboot` | `POST` | Programa reinicio seguro con margen de 10 segundos. |
| `/api/power/cancel` | `POST` | Cancela un apagado o reinicio programado. |
| `/api/power/wake_screen` | `POST` | Despierta los monitores y el compositor DWM. |
| `/api/config` | `GET/POST` | Lee o actualiza los ajustes en caliente. |
| `/api/test_notification` | `POST` | Dispara un mensaje de prueba a `discord`, `telegram` o `whatsapp`. |

---

## FAQ & Solución de Problemas

<details>
<summary><b>1. Python no se reconoce como comando interno o externo</b></summary>
Asegúrate de reinstalar Python desde <a href="https://www.python.org/downloads/">python.org</a> y marcar la casilla <b>"Add Python to PATH"</b> en la primera pantalla del instalador. Reinicia la consola tras completarlo.
</details>

<details>
<summary><b>2. Aparece la alerta del Firewall de Windows</b></summary>
Haz clic en <b>"Permitir acceso"</b> asegurándote de que la casilla <i>"Redes privadas"</i> esté marcada. OpenSentinel necesita escuchar en el puerto 8888 para que puedas conectarte desde tu red local o Tailscale.
</details>

<details>
<summary><b>3. La cámara web muestra pantalla negra en el panel</b></summary>
En Windows 10/11, abre <b>Configuración > Privacidad y Seguridad > Cámara</b> y comprueba que <i>"Permitir que las aplicaciones de escritorio accedan a la cámara"</i> esté activado.
</details>

<details>
<summary><b>4. ¿Cómo compruebo si OpenSentinel está activo en segundo plano?</b></summary>
Abre tu navegador y entra en <a href="http://127.0.0.1:8888">http://127.0.0.1:8888</a>. Si el panel carga, el centinela está protegiendo la estación de trabajo. También puedes verificar el Administrador de Tareas (busca el proceso <code>pythonw.exe</code>).
</details>

---

## Créditos de Ingeniería y Co-Autoría

OpenSentinel ha sido diseñado, construido y fortificado mediante arquitectura de alta fiabilidad por:
* **Alberto Trujillo Mingorance** ([@atrumin16](https://github.com/atrumin16)) — Arquitectura de sistemas, telemetría hardware de bajo nivel, motor forense en RAM y diseño del protocolo DEFCON-1.
* **Claude** ([Anthropic](https://anthropic.com)) — Co-autoría en el diseño de protocolos centinela de confianza cero, pipelines de alerta asíncronos y robustecimiento del código.

---

## Licencia

Distribuido bajo la Licencia **MIT**. Consulta [`LICENSE`](LICENSE) para más información.
