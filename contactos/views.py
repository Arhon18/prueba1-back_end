"""
Módulo de Vistas para la Agenda de Contactos.
Arquitectura MVT (Modelo-Vista-Plantilla) de Django.

"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Contacto
from .forms import ContactoForm


def lista_contactos(request):
    """
    Vista principal que lista los contactos y permite búsqueda por nombre o correo.
    Requerimiento: 'Buscar contactos por nombre o correo'.

    """
    query = request.GET.get('q', '').strip()

    total_contactos = Contacto.objects.count()

    if query:
        # Operador de consulta ORM: busca coincidencias parciales (icontains) en nombre O en correo
        contactos = Contacto.objects.filter(
            Q(nombre__icontains=query) | Q(correo__icontains=query)
        )
        encontrados = contactos.count()
        diferencia = total_contactos - encontrados
    else:
        contactos = Contacto.objects.all()
        encontrados = total_contactos
        diferencia = 0

    # Diccionario de contexto para la plantilla (MVT)
    contexto = {
        'contactos': contactos,
        'query': query,
        'total_contactos': total_contactos,
        'encontrados': encontrados,
        'diferencia': diferencia,
        'hay_busqueda': bool(query),
    }
    return render(request, 'contactos/lista.html', contexto)


def agregar_contacto(request):
    """
    Vista para registrar un nuevo contacto en la agenda.
    Requerimiento: 'Agregar contactos con nombre, teléfono, correo y dirección'.

    """
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nuevo_contacto = form.save()
            # Mensaje de éxito con concatenación/formateo de cadenas
            messages.success(
                request,
                f"¡Contacto '{nuevo_contacto.nombre}' agregado exitosamente!"
            )
            return redirect('lista_contactos')
        else:
            messages.error(
                request,
                "Por favor corrige los errores señalados en el formulario."
            )
    else:
        form = ContactoForm()

    contexto = {
        'form': form,
        'accion': 'Agregar Contacto',
        'subtitulo': 'Ingresa los datos para registrar un nuevo contacto personal.',
    }
    return render(request, 'contactos/form.html', contexto)


def detalle_contacto(request, pk):
    """
    Vista para visualizar los detalles individuales de un contacto.

    """
    contacto = get_object_or_404(Contacto, pk=pk)
    contexto = {
        'contacto': contacto,
    }
    return render(request, 'contactos/detalle.html', contexto)


def editar_contacto(request, pk):
    """
    Vista para editar un contacto existente.

    """
    contacto = get_object_or_404(Contacto, pk=pk)

    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            contacto_editado = form.save()
            messages.success(
                request,
                f"¡Contacto '{contacto_editado.nombre}' actualizado correctamente!"
            )
            return redirect('detalle_contacto', pk=contacto.pk)
        else:
            messages.error(
                request,
                "No fue posible actualizar el contacto. Revisa los datos ingresados."
            )
    else:
        form = ContactoForm(instance=contacto)

    contexto = {
        'form': form,
        'contacto': contacto,
        'accion': 'Editar Contacto',
        'subtitulo': f"Actualizando información de {contacto.nombre}",
    }
    return render(request, 'contactos/form.html', contexto)


def eliminar_contacto(request, pk):
    """
    Vista para eliminar un contacto con confirmación previa.
    """
    contacto = get_object_or_404(Contacto, pk=pk)

    if request.method == 'POST':
        nombre = contacto.nombre
        contacto.delete()
        messages.warning(request, f"El contacto '{nombre}' ha sido eliminado.")
        return redirect('lista_contactos')

    contexto = {
        'contacto': contacto,
    }
    return render(request, 'contactos/confirmar_eliminar.html', contexto)
