from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

# Validador de teléfono estándar internacional o nacional
telefono_validador = RegexValidator(
    regex=r'^\+?1?\d{8,15}$',
    message="El número de teléfono debe tener entre 8 y 15 dígitos. Puede incluir el prefijo '+'."
)

class Categoria(models.Model):
    """
    Categoría o etiqueta para clasificar los contactos (ej. Familia, Trabajo, Amigos, etc.)
    """
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Nombre de Categoría")
    color = models.CharField(max_length=20, default="#0d6efd", verbose_name="Color de Identificación (Hex o Clase)")
    descripcion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Contacto(models.Model):
    """
    Modelo principal para la Agenda de Contactos Personal (Caso 3).
    """
    nombre = models.CharField(max_length=80, verbose_name="Nombre(s)")
    apellido = models.CharField(max_length=80, verbose_name="Apellido(s)")
    email = models.EmailField(max_length=120, unique=True, verbose_name="Correo Electrónico")
    telefono = models.CharField(
        max_length=20, 
        validators=[telefono_validador],
        verbose_name="Teléfono Principal",
        help_text="Ejemplo: +56912345678"
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="contactos",
        verbose_name="Categoría"
    )
    empresa = models.CharField(max_length=100, blank=True, null=True, verbose_name="Empresa / Organización")
    cargo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cargo o Puesto")
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento / Cumpleaños")
    es_favorito = models.BooleanField(default=False, verbose_name="¿Es Contacto Favorito?")
    direccion = models.CharField(max_length=250, blank=True, null=True, verbose_name="Dirección o Domicilio")
    notas = models.TextField(blank=True, null=True, verbose_name="Notas Adicionales")
    
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f"{self.nombre_completo} ({self.email})"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}".strip()

    @property
    def iniciales(self):
        ini_n = self.nombre[0].upper() if self.nombre else ""
        ini_a = self.apellido[0].upper() if self.apellido else ""
        return f"{ini_n}{ini_a}" or "?"

    def dias_para_cumpleanos(self):
        """
        Calcula días restantes para el próximo cumpleaños.
        """
        if not self.fecha_nacimiento:
            return None
        hoy = timezone.now().date()
        prox_cumple = self.fecha_nacimiento.replace(year=hoy.year)
        if prox_cumple < hoy:
            prox_cumple = self.fecha_nacimiento.replace(year=hoy.year + 1)
        return (prox_cumple - hoy).days


class TelefonoSecundario(models.Model):
    """
    Teléfonos adicionales asociados al contacto (permite inlines en Django Admin).
    """
    TIPO_CHOICES = [
        ('movil', 'Móvil / Celular'),
        ('trabajo', 'Trabajo / Oficina'),
        ('casa', 'Casa / Fijo'),
        ('otro', 'Otro'),
    ]
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, related_name="telefonos_secundarios", verbose_name="Contacto")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='movil', verbose_name="Tipo")
    numero = models.CharField(max_length=20, validators=[telefono_validador], verbose_name="Número de Teléfono")

    class Meta:
        verbose_name = "Teléfono Secundario"
        verbose_name_plural = "Teléfonos Secundarios"

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.numero}"


class NotaContacto(models.Model):
    """
    Bitácora o notas fechadas asociadas a un contacto (inline en Django Admin).
    """
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE, related_name="bitacora_notas", verbose_name="Contacto")
    titulo = models.CharField(max_length=100, verbose_name="Título o Asunto")
    detalle = models.TextField(verbose_name="Detalle de la Nota")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Nota de Contacto"
        verbose_name_plural = "Bitácora de Notas"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.titulo} ({self.fecha_registro.strftime('%d/%m/%Y')})"
