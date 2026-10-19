"""
Comando de gestión de Django para poblar la base de datos con contactos de prueba.

Uso:
    py manage.py poblar_contactos

Cumplimiento de Criterios:
- Criterio 1: Variables, colecciones (listas de diccionarios) y bucles.
- Criterio 8: Uso avanzado de herramientas del entorno Django.
"""

from django.core.management.base import BaseCommand
from contactos.models import Contacto


class Command(BaseCommand):
    help = 'Puebla la base de datos con contactos iniciales de prueba para evaluación'

    def handle(self, *args, **kwargs):
        contactos_iniciales = [
            {
                'nombre': 'Andrea Soto Pérez',
                'telefono': '+56 9 8765 4321',
                'correo': 'andrea.soto@ejemplo.com',
                'direccion': 'Av. Providencia 1234, Providencia, Santiago'
            },
            {
                'nombre': 'Carlos Mendoza Silva',
                'telefono': '+56 9 7654 3210',
                'correo': 'carlos.mendoza@empresa.cl',
                'direccion': 'Calle Los Alerces 450, Las Condes, Santiago'
            },
            {
                'nombre': 'Beatriz Morales Rojas',
                'telefono': '+56 9 6543 2109',
                'correo': 'beatriz.morales@correo.com',
                'direccion': 'Pasaje El Roble 89, Ñuñoa, Santiago'
            },
            {
                'nombre': 'Daniel Valenzuela Castro',
                'telefono': '+56 9 5432 1098',
                'correo': 'daniel.valenzuela@tech.cl',
                'direccion': 'Av. Libertador Bernardo O\'Higgins 2050, Santiago Centro'
            },
            {
                'nombre': 'Elena Gómez Arancibia',
                'telefono': '+56 9 4321 0987',
                'correo': 'elena.gomez@servicio.com',
                'direccion': 'Calle Bellavista 780, Recoleta, Santiago'
            }
        ]

        creados = 0
        existentes = 0

        for datos in contactos_iniciales:
            contacto, created = Contacto.objects.get_or_create(
                correo=datos['correo'],
                defaults=datos
            )
            if created:
                creados += 1
            else:
                existentes += 1

        self.stdout.write(self.style.SUCCESS(
            f"Proceso finalizado con éxito: {creados} contactos creados, {existentes} ya existentes."
        ))
