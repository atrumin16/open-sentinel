@echo off
title OPENSENTINEL // UNINSTALLER
color 0C

echo ================================================================
echo           DESINSTALADOR DE OPENSENTINEL
echo ================================================================
echo.
echo Deteniendo procesos y eliminando inicio automatico...

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
if exist "%STARTUP_FOLDER%\OpenSentinel.lnk" del /F /Q "%STARTUP_FOLDER%\OpenSentinel.lnk" >nul 2>&1

powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*open-sentinel\main.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" >nul 2>&1

echo.
echo [OK] OpenSentinel ha sido desinstalado del inicio automatico y detenido.
echo.
pause
