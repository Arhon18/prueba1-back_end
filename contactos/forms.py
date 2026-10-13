"""
Módulo de Formularios para la Agenda de Contactos.

"""

from django import forms
from django.core.exceptions import ValidationError
from email_validator import validate_email, EmailNotValidError
# [Criterio 1.1.3] Uso de paquete externo 'phonenumbers'
import phonenumbers
from phonenumbers import NumberParseException

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
                'placeholder': 'Ej. +56 9 8765 4321 o +1 415 555 2671',
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
        """
        [Criterio 1.1.2 y 1.1.3] Validación y normalización con paquete externo 'phonenumbers'.
        Reglas de negocio:
        1. Números Chilenos: Se aceptan con prefijo '+56' o formato nacional (9 dígitos, ej: 912345678).
        2. Números Extranjeros: Es OBLIGATORIO que comiencen con '+' seguido del código de país (ej: +1..., +34...).
        3. Siempre se normaliza y guarda en formato estándar internacional: '+56 9 8765 4321'.
        """
        telefono_raw = self.cleaned_data.get('telefono', '').strip()

        if not telefono_raw:
            raise ValidationError("El número telefónico es obligatorio.")

        # Estructura de decisión: Comprobar si incluye prefijo internacional '+'
        if telefono_raw.startswith('+'):
            # Validación para números con código de país explícito (Chile con +56 o extranjero)
            try:
                numero_parseado = phonenumbers.parse(telefono_raw, None)
                if not phonenumbers.is_valid_number(numero_parseado):
                    raise ValidationError(
                        "Número internacional no válido. Verifica el código de país y la cantidad de dígitos."
                    )
                # Formato internacional estandarizado (+56 9 1234 5678, +1 415 555 2671)
                return phonenumbers.format_number(
                    numero_parseado,
                    phonenumbers.PhoneNumberFormat.INTERNATIONAL
                )
            except NumberParseException:
                raise ValidationError(
                    "Formato de número internacional inválido. Debe iniciar con '+' y su código de país (ej: +56 9 8765 4321 o +1 415 555 2671)."
                )
        else:
            # No incluye '+'. Solo se permite si es un número válido chileno (móvil o fijo)
            try:
                numero_parseado = phonenumbers.parse(telefono_raw, "CL")
                # Comprobar si es un número válido chileno (código de país 56)
                if phonenumbers.is_valid_number(numero_parseado) and numero_parseado.country_code == 56:
                    return phonenumbers.format_number(
                        numero_parseado,
                        phonenumbers.PhoneNumberFormat.INTERNATIONAL
                    )
                else:
                    raise ValidationError(
                        "Número inválido. Si es un número chileno, debe tener 9 dígitos (ej: 912345678). "
                        "Si es un número extranjero, DEBE comenzar obligatoriamente con '+' y el código de país (ej: +1 415 555 2671)."
                    )
            except NumberParseException:
                raise ValidationError(
                    "Número de teléfono inválido. Para números extranjeros debes incluir '+' y el código de país. "
                    "Para números chilenos ingresa 9 dígitos (ej: 912345678 o +56 9 1234 5678)."
                )

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
