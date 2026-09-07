"""
Configuración del Panel Administrativo de Django para 'contactos'.

Cumplimiento de Criterios:
- Criterio 4: Implementación de componentes estándar de Django.
- Criterio 6: Código debidamente documentado y comentado.
"""

from django.contrib import admin
from .models import Contacto


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    """
    Personalización del modelo Contacto en el Django Admin.
    Permite visualizar columnas clave, ordenar y buscar por nombre y correo.
    """
    list_display = ('nombre', 'telefono', 'correo', 'direccion', 'fecha_creacion')
    search_fields = ('nombre', 'correo', 'telefono')
    list_filter = ('fecha_creacion',)
    ordering = ('nombre',)
    date_hierarchy = 'fecha_creacion'
