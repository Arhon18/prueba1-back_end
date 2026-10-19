<<<<<<< HEAD
"""
Configuración avanzada de Django Admin para la aplicación Agenda de Contactos Personal (Caso 3).
Incluye:
- Búsqueda por nombre y email
- Exportación a CSV vía admin.action
- Filtros personalizados con SimpleListFilter
- Inlines para Teléfono Secundario y Bitácora de Notas
- Personalización de branding (site_header, site_title, index_title)
"""
import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import Contacto, Categoria, TelefonoSecundario, NotaContacto

# ==============================================================================
# 1. BRANDING Y PERSONALIZACIÓN DE DJANGO ADMIN
# ==============================================================================
admin.site.site_header = "Agenda Personal | Panel Administrativo"
admin.site.site_title = "Agenda de Contactos"
admin.site.index_title = "Gestión Integral de Contactos Personales"


# ==============================================================================
# 2. ACCIÓN MASIVA: EXPORTAR A CSV (Requerimiento explícito Caso 3)
# ==============================================================================
@admin.action(description="Exportar contactos seleccionados a CSV")
def exportar_contactos_csv(modeladmin, request, queryset):
    """
    Genera un archivo CSV con los datos de los contactos seleccionados.
    """
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="contactos_agenda.csv"'
    response.write('\ufeff')  # BOM para compatibilidad con Excel

    writer = csv.writer(response)
    writer.writerow([
        "ID", "Nombre", "Apellido", "Email", "Teléfono", 
        "Categoría", "Empresa", "Cargo", "Es Favorito", 
        "Fecha Nacimiento", "Fecha Registro"
    ])

    for c in queryset.select_related('categoria'):
        writer.writerow([
            c.id,
            c.nombre,
            c.apellido,
            c.email,
            c.telefono,
            c.categoria.nombre if c.categoria else "Sin categoría",
            c.empresa or "",
            c.cargo or "",
            "Sí" if c.es_favorito else "No",
            c.fecha_nacimiento.strftime("%Y-%m-%d") if c.fecha_nacimiento else "",
            c.fecha_creacion.strftime("%Y-%m-%d %H:%M"),
=======
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
>>>>>>> 608b130aaff29eebc63ffd6d14385d2a72557e80
        ])

    return response


<<<<<<< HEAD
@admin.action(description="Marcar como favoritos los contactos seleccionados")
def marcar_como_favorito(modeladmin, request, queryset):
    actualizados = queryset.update(es_favorito=True)
    modeladmin.message_user(request, f"{actualizados} contacto(s) marcado(s) como favorito(s).")


@admin.action(description="Desmarcar como favoritos")
def desmarcar_como_favorito(modeladmin, request, queryset):
    actualizados = queryset.update(es_favorito=False)
    modeladmin.message_user(request, f"{actualizados} contacto(s) desmarcado(s) de favoritos.")


# ==============================================================================
# 3. FILTROS PERSONALIZADOS (SimpleListFilter)
# ==============================================================================
class CumpleanosMesFilter(admin.SimpleListFilter):
    title = 'cumpleaños este mes'
    parameter_name = 'cumple_mes'

    def lookups(self, request, model_admin):
        return (
            ('este_mes', 'Cumpleañeros del mes en curso'),
            ('con_fecha', 'Con fecha de nacimiento registrada'),
            ('sin_fecha', 'Sin fecha de nacimiento'),
        )

    def queryset(self, request, queryset):
        from django.utils import timezone
        mes_actual = timezone.now().month
        if self.value() == 'este_mes':
            return queryset.filter(fecha_nacimiento__month=mes_actual)
        elif self.value() == 'con_fecha':
            return queryset.filter(fecha_nacimiento__isnull=False)
        elif self.value() == 'sin_fecha':
            return queryset.filter(fecha_nacimiento__isnull=True)
        return queryset


class TieneNotasFilter(admin.SimpleListFilter):
    title = 'bitácora de notas'
    parameter_name = 'tiene_notas'

    def lookups(self, request, model_admin):
        return (
            ('con_notas', 'Con notas registradas'),
            ('sin_notas', 'Sin notas'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'con_notas':
            return queryset.filter(bitacora_notas__isnull=False).distinct()
        if self.value() == 'sin_notas':
            return queryset.filter(bitacora_notas__isnull=True)
        return queryset


# ==============================================================================
# 4. INLINES PARA EL MODELO CONTACTO
# ==============================================================================
class TelefonoSecundarioInline(admin.TabularInline):
    model = TelefonoSecundario
    extra = 1
    classes = ('collapse',)


class NotaContactoInline(admin.StackedInline):
    model = NotaContacto
    extra = 1
    classes = ('collapse',)


# ==============================================================================
# 5. MODELADMINS
# ==============================================================================
@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_completo_display', 
        'email', 
        'telefono', 
        'categoria_badge', 
        'empresa', 
        'es_favorito_icon', 
        'fecha_creacion'
    )
    # Búsqueda exigida: por nombre/email
    search_fields = ('nombre', 'apellido', 'email', 'telefono', 'empresa')
    list_filter = ('es_favorito', 'categoria', CumpleanosMesFilter, TieneNotasFilter, 'fecha_creacion')
    ordering = ('apellido', 'nombre')
    list_per_page = 20
    actions = [exportar_contactos_csv, marcar_como_favorito, desmarcar_como_favorito]
    inlines = [TelefonoSecundarioInline, NotaContactoInline]

    fieldsets = (
        ('Información Personal Básica', {
            'fields': (('nombre', 'apellido'), ('email', 'telefono'), 'es_favorito')
        }),
        ('Clasificación y Trabajo', {
            'fields': (('categoria', 'empresa', 'cargo'),)
        }),
        ('Detalles y Domicilio', {
            'fields': (('fecha_nacimiento', 'direccion'), 'notas'),
=======
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
>>>>>>> 608b130aaff29eebc63ffd6d14385d2a72557e80
            'classes': ('collapse',),
        }),
    )

<<<<<<< HEAD
    @admin.display(description="Nombre Completo", ordering="apellido")
    def nombre_completo_display(self, obj):
        return obj.nombre_completo

    @admin.display(description="Categoría", ordering="categoria__nombre")
    def categoria_badge(self, obj):
        if obj.categoria:
            return obj.categoria.nombre
        return "-"

    @admin.display(description="Favorito", boolean=True, ordering="es_favorito")
    def es_favorito_icon(self, obj):
        return obj.es_favorito

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('categoria')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'color', 'descripcion', 'total_contactos')
    search_fields = ('nombre', 'descripcion')

    @admin.display(description="Total de Contactos")
    def total_contactos(self, obj):
        return obj.contactos.count()


@admin.register(TelefonoSecundario)
class TelefonoSecundarioAdmin(admin.ModelAdmin):
    list_display = ('contacto', 'tipo', 'numero')
    search_fields = ('contacto__nombre', 'contacto__apellido', 'contacto__email', 'numero')
    list_filter = ('tipo',)
=======
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
>>>>>>> 608b130aaff29eebc63ffd6d14385d2a72557e80


@admin.register(NotaContacto)
class NotaContactoAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    list_display = ('contacto', 'titulo', 'fecha_registro')
    search_fields = ('contacto__nombre', 'contacto__apellido', 'titulo', 'detalle')
    list_filter = ('fecha_registro',)
    date_hierarchy = 'fecha_registro'
=======
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
>>>>>>> 608b130aaff29eebc63ffd6d14385d2a72557e80
