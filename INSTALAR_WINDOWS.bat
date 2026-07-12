@echo off
title PORTES AI SPORTS - Instalacion
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
echo.
echo Instalacion terminada.
echo Para iniciar, ejecute INICIAR_WINDOWS.bat
pause
