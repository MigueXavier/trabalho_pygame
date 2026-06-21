@echo off
cd /d "%~dp0"
title Perdido no Algoritmo

python --version >nul 2>&1
if %errorlevel%==0 goto temPython

echo Python nao encontrado. Instalando via winget...
winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
if %errorlevel% neq 0 (
    echo.
    echo Falha ao instalar o Python automaticamente.
    echo Instale manualmente em https://www.python.org/downloads/ e rode de novo.
    pause
    exit /b 1
)
echo.
echo Python instalado. FECHE esta janela e rode o jogar.bat novamente.
pause
exit /b 0

:temPython
echo Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Iniciando o jogo...
python main.py
pause
