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
        ])

    return response


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
            'classes': ('collapse',),
        }),
    )

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


@admin.register(NotaContacto)
class NotaContactoAdmin(admin.ModelAdmin):
    list_display = ('contacto', 'titulo', 'fecha_registro')
    search_fields = ('contacto__nombre', 'contacto__apellido', 'titulo', 'detalle')
    list_filter = ('fecha_registro',)
    date_hierarchy = 'fecha_registro'
