import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import Contacto


@admin.action(description="Exportar contactos seleccionados a CSV")
def exportar_contactos_a_csv(modeladmin, request, queryset):
    """
    Acción personalizada de Django Admin para exportar los contactos seleccionados a formato CSV.
    Requerimiento Caso 3: exportación simple (action) a CSV.
    """
    response = HttpResponse(
        content_type='text/csv; charset=utf-8-sig',
    )
    response['Content-Disposition'] = 'attachment; filename="contactos_agenda.csv"'

    writer = csv.writer(response)
    # Escribir encabezados
    writer.writerow([
        'ID',
        'Nombre Completo',
        'Teléfono',
        'Correo Electrónico',
        'Dirección',
        'Fecha de Creación',
        'Última Actualización'
    ])

    # Escribir filas de datos
    for contacto in queryset:
        writer.writerow([
            contacto.id,
            contacto.nombre,
            contacto.telefono,
            contacto.correo,
            contacto.direccion,
            contacto.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if contacto.fecha_creacion else '',
            contacto.fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S') if contacto.fecha_actualizacion else ''
        ])

    return response


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    """
    Personalización del modelo Contacto en el Django Admin.
    Requerimientos Caso 3:
    - Búsqueda por nombre y email.
    - Exportación simple (action) a CSV.
    - Filtros por fecha de creación y actualización.
    - List display con columnas clave.
    """
    list_display = (
        'nombre',
        'telefono',
        'correo',
        'direccion',
        'fecha_creacion',
        'fecha_actualizacion'
    )
    search_fields = ('nombre', 'correo', 'telefono')
    list_filter = ('fecha_creacion', 'fecha_actualizacion')
    ordering = ('nombre',)
    date_hierarchy = 'fecha_creacion'
    list_per_page = 20
    actions = [exportar_contactos_a_csv]


# Personalización del Branding de Django Admin (Requerimiento ES02)
admin.site.site_header = "Panel de Control - Agenda de Contactos"
admin.site.site_title = "Agenda de Contactos Admin"
admin.site.index_title = "Administración de Contactos Personales"
