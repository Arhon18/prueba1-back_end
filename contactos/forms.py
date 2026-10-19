"""
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
