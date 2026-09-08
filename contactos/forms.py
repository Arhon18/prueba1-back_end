"""
Módulo de Formularios para la Agenda de Contactos.

"""

from django import forms
from django.core.exceptions import ValidationError
from email_validator import validate_email, EmailNotValidError

from .models import Contacto


class ContactoForm(forms.ModelForm):

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
        
        nombre = self.cleaned_data.get('nombre', '').strip()

        # Estructura de decisión con operador de comparación
        if len(nombre) < 3:
            raise ValidationError("El nombre debe tener al menos 3 caracteres.")

        # Operación: Capitalización adecuada de cada palabra
        return nombre.title()

    def clean_telefono(self):
       
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
        
        correo = self.cleaned_data.get('correo', '').strip().lower()

        # Estructura de decisión previa: comprobación de contenido
        if not correo:
            raise ValidationError("El correo electrónico es obligatorio.")

        try:
            info_email = validate_email(correo, check_deliverability=False)
            correo_normalizado = info_email.normalized
            return correo_normalizado
        except EmailNotValidError as e:
            raise ValidationError(f"Formato de correo electrónico inválido: {str(e)}")

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '').strip()
        if len(direccion) < 5:
            raise ValidationError("La dirección debe contener al menos 5 caracteres.")
        return direccion
