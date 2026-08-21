@echo off
setlocal enabledelayedexpansion
title OPENSENTINEL // 2-CLICK INSTALLER
color 0B

echo ================================================================
echo           OPENSENTINEL // INSTALADOR EN 2 CLICS
echo ================================================================
echo.

:: 1. Comprobar Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo [ERROR] Python no esta instalado o no se encuentra en el PATH.
    echo Descarga e instala Python 3.10+ marcando "Add Python to PATH":
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

set "ROOT_DIR=%~dp0.."
pushd "%ROOT_DIR%"

echo [1/4] Verificando e instalando dependencias de Python...
pip install -r requirements.txt --quiet
if %ERRORLEVEL% NEQ 0 (
    echo [AVISO] Intentando instalacion directa de paquetes...
    pip install flask psutil pillow requests opencv-python numpy python-dotenv --quiet
)
echo [OK] Dependencias listas.
echo.

:: 2. Crear config.json si no existe
if not exist "config.json" (
    echo [2/4] Creando plantilla de configuracion config.json...
    copy "config.example.json" "config.json" >nul
) else (
    echo [2/4] Archivo config.json existente verificado.
)
echo.

:: 3. Configurar Inicio Automatico Silencioso de Windows
echo [3/4] Configurando arranque silencioso de Windows...
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
if exist "%STARTUP_FOLDER%\OpenSentinel.lnk" del /F /Q "%STARTUP_FOLDER%\OpenSentinel.lnk" >nul 2>&1

powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%STARTUP_FOLDER%\OpenSentinel.lnk'); $s.TargetPath = 'wscript.exe'; $s.Arguments = '\"%ROOT_DIR%\scripts\run_hidden.vbs\"'; $s.WorkingDirectory = '%ROOT_DIR%'; $s.Description = 'OpenSentinel Background Service'; $s.Save()"
echo [OK] Acceso en Inicio configurado.
echo.

:: 4. Detener instancias previas e iniciar
echo [4/4] Iniciando OpenSentinel en segundo plano...
powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*open-sentinel\main.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" >nul 2>&1
wscript.exe "%ROOT_DIR%\scripts\run_hidden.vbs"
timeout /t 2 /nobreak >nul

popd

color 0A
echo ================================================================
echo           INSTALACION DE OPENSENTINEL COMPLETADA
echo ================================================================
echo.
echo  * Panel Local:       http://127.0.0.1:8888
echo  * Alertas Multi-Canal: Discord, Telegram y WhatsApp
echo  * Arranque de Windows: Activo en segundo plano (0%% CPU residual)
echo.
echo ================================================================
echo  Presiona cualquier tecla para finalizar.
echo ================================================================
pause >nul
