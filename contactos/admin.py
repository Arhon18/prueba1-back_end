import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.html import format_html
from django.urls import reverse
from .models import Contacto, NotaContacto


class NotaContactoInline(admin.TabularInline):
    """
    Inline para gestionar las notas y observaciones directamente
    desde la pantalla de edición del Contacto.
    Cumple con el criterio de 'inlines cuando corresponde'.
    """
    model = NotaContacto
    extra = 1
    classes = ('collapse',)
    fields = ('titulo', 'contenido', 'es_importante', 'fecha_creacion')
    readonly_fields = ('fecha_creacion',)


@admin.action(description="📥 Exportar contactos seleccionados a CSV")
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
    writer.writerow([
        'ID',
        'Nombre Completo',
        'Teléfono',
        'Correo Electrónico',
        'Dirección',
        'Total de Notas',
        'Fecha de Creación',
        'Última Actualización'
    ])

    for contacto in queryset:
        writer.writerow([
            contacto.id,
            contacto.nombre,
            contacto.telefono,
            contacto.correo,
            contacto.direccion,
            contacto.notas.count(),
            contacto.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S') if contacto.fecha_creacion else '',
            contacto.fecha_actualizacion.strftime('%Y-%m-%d %H:%M:%S') if contacto.fecha_actualizacion else ''
        ])

    return response


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    """
    Personalización avanzada del modelo Contacto en Django Admin:
    - Búsqueda multifactorial por nombre, correo y teléfono.
    - Exportación masiva a CSV (Requerimiento Caso 3).
    - Inlines de notas relacionales (NotaContactoInline).
    - Fieldsets organizados con diseño moderno.
    - Badges HTML con enlaces y badges de conteo.
    """
    inlines = [NotaContactoInline]
    actions = [exportar_contactos_a_csv]

    class Media:
        css = {
            'all': ('contactos/css/custom_admin.css',)
        }

    list_display = (
        'nombre_badge',
        'telefono_link',
        'correo_link',
        'direccion',
        'total_notas_badge',
        'fecha_creacion_formateada',
    )
    list_display_links = ('nombre_badge',)
    search_fields = ('nombre', 'correo', 'telefono', 'direccion')
    list_filter = ('fecha_creacion', 'fecha_actualizacion')
    ordering = ('nombre',)
    date_hierarchy = 'fecha_creacion'
    list_per_page = 20
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'ver_en_web')

    fieldsets = (
        ('Identificación del Contacto', {
            'fields': (('nombre', 'correo'), 'telefono', 'direccion'),
            'description': 'Información principal del contacto personal.'
        }),
        ('Metadatos del Registro', {
            'fields': (('fecha_creacion', 'fecha_actualizacion'), 'ver_en_web'),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description="Nombre", ordering="nombre")
    def nombre_badge(self, obj):
        inicial = obj.nombre[:1].upper() if obj.nombre else "?"
        return format_html(
            '<div style="display: inline-flex; align-items: center; gap: 8px;">'
            '<span style="background: #2563eb; color: #fff; width: 26px; height: 26px; '
            'border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; '
            'font-size: 11px; font-weight: bold;">{}</span>'
            '<strong style="color: #1e293b; font-size: 13px;">{}</strong>'
            '</div>',
            inicial,
            obj.nombre
        )

    @admin.display(description="Teléfono")
    def telefono_link(self, obj):
        return format_html(
            '<a href="tel:{}" style="text-decoration: none; color: #059669; font-weight: 500;">'
            '📞 {}</a>',
            obj.telefono,
            obj.telefono
        )

    @admin.display(description="Correo Electrónico")
    def correo_link(self, obj):
        return format_html(
            '<a href="mailto:{}" style="text-decoration: none; color: #2563eb; font-weight: 500;">'
            '✉️ {}</a>',
            obj.correo,
            obj.correo
        )

    @admin.display(description="Notas")
    def total_notas_badge(self, obj):
        count = obj.notas.count()
        bg_color = "#3b82f6" if count > 0 else "#94a3b8"
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600;">'
            '📝 {} nota{}</span>',
            bg_color,
            count,
            's' if count != 1 else ''
        )

    @admin.display(description="Registrado", ordering="fecha_creacion")
    def fecha_creacion_formateada(self, obj):
        return obj.fecha_creacion.strftime('%d/%m/%Y %H:%M') if obj.fecha_creacion else '-'

    @admin.display(description="Acceso en Aplicación Web")
    def ver_en_web(self, obj):
        if obj.pk:
            url = reverse('detalle_contacto', kwargs={'pk': obj.pk})
            return format_html(
                '<a href="{}" target="_blank" style="display: inline-block; padding: 6px 12px; background: #2563eb; color: white; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 12px;">'
                '🌐 Ver ficha pública de {} en la Agenda &rarr;</a>',
                url,
                obj.nombre
            )
        return "Guarda el contacto para generar enlace."


@admin.register(NotaContacto)
class NotaContactoAdmin(admin.ModelAdmin):
    """
    Administración independiente para las notas de contactos.
    Permite filtrar por prioridad y buscar por contacto.
    """
    class Media:
        css = {
            'all': ('contactos/css/custom_admin.css',)
        }

    list_display = ('titulo', 'contacto', 'es_importante_badge', 'fecha_creacion')
    list_filter = ('es_importante', 'fecha_creacion')
    search_fields = ('titulo', 'contenido', 'contacto__nombre', 'contacto__correo')
    autocomplete_fields = ('contacto',)
    list_per_page = 20

    @admin.display(description="Prioridad", ordering="es_importante")
    def es_importante_badge(self, obj):
        if obj.es_importante:
            return format_html(
                '<span style="background: #ef4444; color: white; padding: 2px 7px; border-radius: 8px; font-size: 11px; font-weight: bold;">⭐ Importante</span>'
            )
        return format_html(
            '<span style="background: #e2e8f0; color: #475569; padding: 2px 7px; border-radius: 8px; font-size: 11px;">Normal</span>'
        )


# Personalización del Branding de Django Admin (Requerimiento ES02)
admin.site.site_header = "Panel de Control - Agenda de Contactos"
admin.site.site_title = "Agenda de Contactos Admin"
admin.site.index_title = "Administración de Contactos Personales"
