@echo off
title INICIAR OPENSENTINEL
wscript.exe "%~dp0run_hidden.vbs"
echo [OK] OpenSentinel iniciado en segundo plano.
timeout /t 2 /nobreak >nul
