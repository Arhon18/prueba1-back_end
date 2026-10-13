#!/bin/bash
# Script de construcción para Vercel
echo "==> Instalando dependencias..."
python3 -m pip install -r requirements.txt

echo "==> Recolectando archivos estáticos con WhiteNoise..."
python3 manage.py collectstatic --noinput --clear

echo "==> Ejecutando migraciones de base de datos..."
python3 manage.py migrate --noinput

echo "==> Despliegue listo."
