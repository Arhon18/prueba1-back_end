"""
<<<<<<< HEAD
Formularios para el módulo de Contactos con validaciones robustas y estilos Bootstrap 5
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Contacto, Categoria, TelefonoSecundario, NotaContacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = [
            'nombre', 'apellido', 'email', 'telefono', 
            'categoria', 'empresa', 'cargo', 
            'fecha_nacimiento', 'es_favorito', 'direccion', 'notas'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Carlos'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. González'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56912345678'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Empresa o Institución'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Desarrollador, Gerente'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle, Número, Ciudad'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Información relevante sobre el contacto...'}),
            'es_favorito': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        # Verificar duplicados excluyendo la instancia actual si es edición
        qs = Contacto.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("Ya existe un contacto registrado con este correo electrónico.")
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip().replace(" ", "").replace("-", "")
        if len(telefono) < 8:
            raise ValidationError("El teléfono debe contener al menos 8 dígitos.")
        return telefono


class TelefonoSecundarioForm(forms.ModelForm):
    class Meta:
        model = TelefonoSecundario
        fields = ['tipo', 'numero']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56987654321'}),
        }


class NotaContactoForm(forms.ModelForm):
    class Meta:
        model = NotaContacto
        fields = ['titulo', 'detalle']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto o motivo'}),
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Escribe una nota rápida...'}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'color', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'color': forms.TextInput(attrs={'class': 'form-control form-control-color', 'type': 'color'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breve descripción'}),
        }
=======
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
>>>>>>> 608b130aaff29eebc63ffd6d14385d2a72557e80
