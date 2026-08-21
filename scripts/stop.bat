@echo off
title DETENER OPENSENTINEL
powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*open-sentinel\main.py*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }" >nul 2>&1
echo [OK] OpenSentinel detenido.
timeout /t 2 /nobreak >nul
