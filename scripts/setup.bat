@echo off
title OPENSENTINEL // CONFIGURATION WIZARD
color 0B
set "ROOT_DIR=%~dp0.."
pushd "%ROOT_DIR%"
python main.py --setup
popd
pause
