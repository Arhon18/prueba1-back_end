"""
Módulo de Modelos para la Agenda de Contactos.
Arquitectura MVT (Modelo-Vista-Plantilla) de Django.

"""

from django.db import models
import phonenumbers
from phonenumbers import NumberParseException


class Contacto(models.Model):
    nombre = models.CharField(
        max_length=120,
        verbose_name="Nombre Completo",
        help_text="Nombre y apellido del contacto"
    )
    telefono = models.CharField(
        max_length=30,
        verbose_name="Teléfono",
        help_text="Número chileno (+56 9...) o extranjero obligatorio con prefijo '+' (ej: +1...)"
    )
    correo = models.EmailField(
        max_length=150,
        verbose_name="Correo Electrónico",
        help_text="Dirección de correo electrónico válida"
    )
    direccion = models.CharField(
        max_length=250,
        verbose_name="Dirección",
        help_text="Dirección física o residencia del contacto"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )

    class Meta:
        verbose_name = "Contacto"
        verbose_name_plural = "Contactos"
        ordering = ['nombre']

    def __str__(self):
        # Operación de concatenación de cadenas y formato
        return f"{self.nombre} ({self.correo})"

    def clean(self):
        """
        Normalización de datos antes de guardar.
        Operaciones básicas de strings y normalización telefónica con phonenumbers.
        """
        if self.nombre:
            self.nombre = self.nombre.strip().title()
        if self.telefono:
            tel_clean = self.telefono.strip()
            try:
                if tel_clean.startswith('+'):
                    p = phonenumbers.parse(tel_clean, None)
                else:
                    p = phonenumbers.parse(tel_clean, "CL")
                if phonenumbers.is_valid_number(p):
                    self.telefono = phonenumbers.format_number(
                        p, phonenumbers.PhoneNumberFormat.INTERNATIONAL
                    )
                else:
                    self.telefono = tel_clean
            except NumberParseException:
                self.telefono = tel_clean
        if self.correo:
            self.correo = self.correo.strip().lower()
        if self.direccion:
            self.direccion = self.direccion.strip()
        super().clean()
