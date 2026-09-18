@echo off
title CTF Forense - Servidor Local Offline
cd /d "%~dp0"
echo ========================================================
echo       INICIANDO CTF FORENSE - PLATAFORMA LOCAL
echo ========================================================
echo.
echo Abriendo servidor local en http://localhost:8100 ...
echo.
python server.py
pause
