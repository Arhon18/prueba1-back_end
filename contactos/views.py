"""
Módulo de Vistas para la Agenda de Contactos.
Arquitectura MVT (Modelo-Vista-Plantilla) de Django.
Incluye CRUD completo, validaciones, paginación, búsqueda y feedback al usuario.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import logging

from .models import Contacto
from .forms import ContactoForm

logger = logging.getLogger(__name__)


def lista_contactos(request):
    """
    Vista principal que lista los contactos con paginación y búsqueda por nombre o correo.
    Requerimientos:
    - Búsqueda por nombre o correo.
    - Paginación en listados.
    - Mensajes y feedback.
    """
    query = request.GET.get('q', '').strip()
    total_contactos = Contacto.objects.count()

    if query:
        # Búsqueda insensible a mayúsculas/minúsculas en nombre o correo
        contactos_qs = Contacto.objects.filter(
            Q(nombre__icontains=query) | Q(correo__icontains=query)
        ).order_by('nombre')
        encontrados = contactos_qs.count()
        diferencia = total_contactos - encontrados
        logger.info(f"Búsqueda realizada con término '{query}'. Resultados: {encontrados}")
    else:
        contactos_qs = Contacto.objects.all().order_by('nombre')
        encontrados = total_contactos
        diferencia = 0

    # Paginación: 6 contactos por página
    paginator = Paginator(contactos_qs, 6)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    contexto = {
        'page_obj': page_obj,
        'contactos': page_obj.object_list,
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
    Requerimiento: CRUD - Create con validaciones de datos y manejo de errores.
    """
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            try:
                nuevo_contacto = form.save()
                logger.info(f"Contacto creado exitosamente: ID={nuevo_contacto.id}, Nombre='{nuevo_contacto.nombre}'")
                messages.success(
                    request,
                    f"¡Contacto '{nuevo_contacto.nombre}' registrado exitosamente!"
                )
                return redirect('lista_contactos')
            except Exception as e:
                logger.error(f"Error al guardar contacto: {str(e)}")
                messages.error(
                    request,
                    f"Ocurrió un error al intentar guardar el contacto: {str(e)}"
                )
        else:
            logger.warning("Fallo en la validación del formulario de creación de contacto.")
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
    Requerimiento: CRUD - Read individual.
    """
    contacto = get_object_or_404(Contacto, pk=pk)
    contexto = {
        'contacto': contacto,
    }
    return render(request, 'contactos/detalle.html', contexto)


def editar_contacto(request, pk):
    """
    Vista para actualizar un contacto existente.
    Requerimiento: CRUD - Update con validaciones y control de errores.
    """
    contacto = get_object_or_404(Contacto, pk=pk)

    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            try:
                contacto_editado = form.save()
                logger.info(f"Contacto actualizado exitosamente: ID={contacto_editado.id}")
                messages.success(
                    request,
                    f"¡Contacto '{contacto_editado.nombre}' actualizado correctamente!"
                )
                return redirect('detalle_contacto', pk=contacto.pk)
            except Exception as e:
                logger.error(f"Error al actualizar contacto ID={pk}: {str(e)}")
                messages.error(
                    request,
                    f"Ocurrió un error inesperado al actualizar el contacto: {str(e)}"
                )
        else:
            logger.warning(f"Fallo en la validación al editar contacto ID={pk}.")
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
    Requerimiento: CRUD - Delete con feedback al usuario.
    """
    contacto = get_object_or_404(Contacto, pk=pk)

    if request.method == 'POST':
        nombre = contacto.nombre
        try:
            contacto.delete()
            logger.info(f"Contacto eliminado: '{nombre}' (ID={pk})")
            messages.warning(request, f"El contacto '{nombre}' ha sido eliminado.")
            return redirect('lista_contactos')
        except Exception as e:
            logger.error(f"Error al eliminar contacto ID={pk}: {str(e)}")
            messages.error(
                request,
                f"Error al eliminar el contacto: {str(e)}"
            )
            return redirect('detalle_contacto', pk=pk)

    contexto = {
        'contacto': contacto,
    }
    return render(request, 'contactos/confirmar_eliminar.html', contexto)
