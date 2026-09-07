"""
Módulo de Modelos para la Agenda de Contactos.
Arquitectura MVT (Modelo-Vista-Plantilla) de Django.

Cumplimiento de Criterios:
- Criterio 1.1.1: Identificación y uso de tipos de variables (CharField, EmailField, DateTimeField) y operaciones.
- Criterio 1.1.4: Implementación del Modelo en Django.
"""

from django.db import models


class Contacto(models.Model):
    """
    Modelo que representa a un contacto personal en la agenda.
    Contiene la información de nombre, teléfono, correo electrónico y dirección.
    """
    nombre = models.CharField(
        max_length=120,
        verbose_name="Nombre Completo",
        help_text="Nombre y apellido del contacto"
    )
    telefono = models.CharField(
        max_length=25,
        verbose_name="Teléfono",
        help_text="Número telefónico de contacto (ej: +56 9 1234 5678)"
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
        Operaciones básicas de strings (strip, title, lower).
        """
        if self.nombre:
            self.nombre = self.nombre.strip()
        if self.telefono:
            self.telefono = self.telefono.strip()
        if self.correo:
            self.correo = self.correo.strip().lower()
        if self.direccion:
            self.direccion = self.direccion.strip()
        super().clean()
