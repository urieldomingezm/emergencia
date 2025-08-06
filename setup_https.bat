@echo off
echo 🔐 Configurando HTTPS para Emergency GPS...
echo.

REM Generar certificados SSL
python generate_ssl.py

echo.
echo 🚀 Iniciando aplicación con HTTPS...
docker-compose up --build

pause