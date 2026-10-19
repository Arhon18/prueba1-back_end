#!/bin/bash
set -e

echo "==> Creando entorno virtual..."
python3 -m venv .venv
source .venv/bin/activate

echo "==> Instalando dependencias..."
python -m pip install -r requirements.txt

echo "==> Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "==> Ejecutando migraciones..."
python manage.py migrate --noinput

echo "==> Despliegue listo."