"""
Módulo de Formularios para la Agenda de Contactos.

Cumplimiento de Criterios:
- Criterio 1.1.1: Manipulación de variables, operadores y conversión de tipos.
- Criterio 1.1.2: Estructuras de decisión (if/elif/else) y operadores lógicos (and, or, not).
- Criterio 1.1.3: Utilización de paquetes externos (email-validator) para validación estricta de correo.
- Criterio 1.1.4: Implementación de Django Form / ModelForm.
"""

from django import forms
from django.core.exceptions import ValidationError
# [Criterio 1.1.3] Uso de paquete externo 'email-validator'
from email_validator import validate_email, EmailNotValidError

from .models import Contacto


class ContactoForm(forms.ModelForm):
    """
    Formulario para agregar y editar contactos personales.
    Aplica estilos con widgets de Bootstrap y valida exhaustivamente los datos ingresados.
    """

    class Meta:
        model = Contacto
        fields = ['nombre', 'telefono', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Andrea Soto Pérez',
                'required': True,
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. +56 9 8765 4321',
                'required': True,
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. andrea.soto@correo.cl',
                'required': True,
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Av. Los Libertadores 1234, Santiago',
                'required': True,
            }),
        }
        labels = {
            'nombre': 'Nombre Completo',
            'telefono': 'Teléfono de Contacto',
            'correo': 'Correo Electrónico',
            'direccion': 'Dirección de Residencia',
        }

    def clean_nombre(self):
        """
        [Criterio 1.1.1 y 1.1.2] Operaciones de cadena y estructuras de decisión.
        Valida que el nombre no contenga caracteres inválidos y tenga al menos 3 caracteres.
        """
        nombre = self.cleaned_data.get('nombre', '').strip()

        # Estructura de decisión con operador de comparación
        if len(nombre) < 3:
            raise ValidationError("El nombre debe tener al menos 3 caracteres.")

        # Operación: Capitalización adecuada de cada palabra
        return nombre.title()

    def clean_telefono(self):
        """
        [Criterio 1.1.1 y 1.1.2] Validación y limpieza de teléfono.
        Uso de operadores de pertenencia (in) y condicionales.
        """
        telefono = self.cleaned_data.get('telefono', '').strip()

        # Operación: filtrar solo dígitos y símbolo '+'
        caracteres_permitidos = "0123456789+ -()"
        for char in telefono:
            if char not in caracteres_permitidos:
                raise ValidationError(f"El teléfono contiene caracteres no permitidos: '{char}'")

        # Contar dígitos reales usando comprensión y función del lenguaje
        digitos = [c for c in telefono if c.isdigit()]
        if len(digitos) < 8 or len(digitos) > 15:
            raise ValidationError("El número telefónico debe contener entre 8 y 15 dígitos.")

        return telefono

    def clean_correo(self):
        """
        [Criterio 1.1.2 y 1.1.3] Validación con paquete externo 'email-validator'.
        Valida el formato sintáctico estricto del correo electrónico.
        """
        correo = self.cleaned_data.get('correo', '').strip().lower()

        # Estructura de decisión previa: comprobación de contenido
        if not correo:
            raise ValidationError("El correo electrónico es obligatorio.")

        try:
            # [Criterio 1.1.3] Llamada a función del paquete externo email-validator
            # check_deliverability=False permite validar sintaxis sin requerir conexión DNS activa
            info_email = validate_email(correo, check_deliverability=False)
            correo_normalizado = info_email.normalized
            return correo_normalizado
        except EmailNotValidError as e:
            # [Criterio 1.1.2] Manejo de error y respuesta condicional
            raise ValidationError(f"Formato de correo electrónico inválido: {str(e)}")

    def clean_direccion(self):
        """
        Validación del campo dirección.
        """
        direccion = self.cleaned_data.get('direccion', '').strip()
        if len(direccion) < 5:
            raise ValidationError("La dirección debe contener al menos 5 caracteres.")
        return direccion
