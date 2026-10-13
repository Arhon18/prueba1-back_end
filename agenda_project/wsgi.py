"""
WSGI config for agenda_project project.

It exposes the WSGI callable as a module-level variable named ``application``.
Soporta exportación de 'app' para compatibilidad con Vercel Serverless Functions.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agenda_project.settings')

application = get_wsgi_application()

# Alias 'app' requerido por entornos serverless como Vercel
app = application
