"""
<<<<<<< HEAD
Vistas CRUD completas para la Agenda de Contactos Personal (Caso 3).
Incluye:
- Listado con filtros, búsqueda, orden y paginación
- Creación y edición con feedback y validaciones
- Detalle con gestión de teléfonos secundarios y notas
- Eliminación con confirmación
- Acción de toggle favorito
- Exportación CSV desde la web y gestión de categorías
"""
import csv
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.utils import timezone

from .models import Contacto, Categoria, TelefonoSecundario, NotaContacto
from .forms import ContactoForm, TelefonoSecundarioForm, NotaContactoForm, CategoriaForm


# ==============================================================================
# 1. LISTADO DE CONTACTOS (R)
# ==============================================================================
def contacto_list(request):
    """
    Listado principal de contactos con búsqueda, filtrado por categorías,
    favoritos, paginación y métricas de resumen.
    """
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')
    solo_favoritos = request.GET.get('favoritos', '')
    orden = request.GET.get('orden', 'nombre')

    contactos = Contacto.objects.select_related('categoria').all()

    # Filtro por búsqueda de texto (nombre, apellido, email, teléfono, empresa)
    if query:
        contactos = contactos.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(email__icontains=query) |
            Q(telefono__icontains=query) |
            Q(empresa__icontains=query)
        )

    # Filtro por categoría
    if categoria_id:
        contactos = contactos.filter(categoria_id=categoria_id)

    # Filtro por favoritos
    if solo_favoritos == '1':
        contactos = contactos.filter(es_favorito=True)

    # Ordenamiento
    if orden == 'apellido':
        contactos = contactos.order_by('apellido', 'nombre')
    elif orden == 'recientes':
        contactos = contactos.order_by('-fecha_creacion')
    else:
        contactos = contactos.order_by('nombre', 'apellido')

    # Métricas y resumen
    total_contactos = Contacto.objects.count()
    total_favoritos = Contacto.objects.filter(es_favorito=True).count()
    total_categorias = Categoria.objects.count()

    # Cumpleaños de este mes
    mes_actual = timezone.now().month
    cumpleaneros_mes = Contacto.objects.filter(fecha_nacimiento__month=mes_actual).count()

    # Paginación (10 contactos por página)
    paginator = Paginator(contactos, 9)
    page_number = request.GET.get('page')
    contactos_page = paginator.get_page(page_number)

    categorias = Categoria.objects.annotate(num_contactos=Count('contactos')).all()

    context = {
        'contactos': contactos_page,
        'categorias': categorias,
        'query': query,
        'categoria_id': categoria_id,
        'solo_favoritos': solo_favoritos,
        'orden': orden,
        'total_contactos': total_contactos,
        'total_favoritos': total_favoritos,
        'total_categorias': total_categorias,
        'cumpleaneros_mes': cumpleaneros_mes,
    }
    return render(request, 'contactos/contacto_list.html', context)


# ==============================================================================
# 2. CREAR CONTACTO (C)
# ==============================================================================
def contacto_create(request):
    """
    Registra un nuevo contacto con validaciones de formulario y mensajes flash.
=======
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
>>>>>>> 608b130aaff29eebc63ffd6d14385d2a72557e80
    """
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
<<<<<<< HEAD
            contacto = form.save()
            messages.success(request, f'¡Contacto "{contacto.nombre_completo}" creado exitosamente!')
            return redirect('contacto_detail', pk=contacto.pk)
        else:
            messages.error(request, 'Por favor revisa los errores señalados en el formulario.')
    else:
        form = ContactoForm()

    return render(request, 'contactos/contacto_form.html', {
        'form': form,
        'titulo': 'Nuevo Contacto',
        'subtitulo': 'Ingresa los datos personales del nuevo contacto'
    })


# ==============================================================================
# 3. DETALLE DE CONTACTO Y GESTIÓN DE RELACIONES
# ==============================================================================
def contacto_detail(request, pk):
    """
    Ficha completa del contacto con teléfonos secundarios y bitácora de notas.
    """
    contacto = get_object_or_404(
        Contacto.objects.select_related('categoria').prefetch_related('telefonos_secundarios', 'bitacora_notas'), 
        pk=pk
    )

    telefono_form = TelefonoSecundarioForm()
    nota_form = NotaContactoForm()

    return render(request, 'contactos/contacto_detail.html', {
        'contacto': contacto,
        'telefono_form': telefono_form,
        'nota_form': nota_form,
    })


# ==============================================================================
# 4. ACTUALIZAR CONTACTO (U)
# ==============================================================================
def contacto_update(request, pk):
    """
    Modifica los datos de un contacto existente.
    """
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            contacto = form.save()
            messages.success(request, f'¡Contacto "{contacto.nombre_completo}" actualizado correctamente!')
            return redirect('contacto_detail', pk=contacto.pk)
        else:
            messages.error(request, 'Corrige los errores antes de guardar.')
    else:
        form = ContactoForm(instance=contacto)

    return render(request, 'contactos/contacto_form.html', {
        'form': form,
        'contacto': contacto,
        'titulo': f'Editar Contacto: {contacto.nombre_completo}',
        'subtitulo': 'Actualiza la información del contacto'
    })


# ==============================================================================
# 5. ELIMINAR CONTACTO (D)
# ==============================================================================
def contacto_delete(request, pk):
    """
    Elimina un contacto previa confirmación explícita del usuario.
    """
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        nombre_completo = contacto.nombre_completo
        contacto.delete()
        messages.success(request, f'El contacto "{nombre_completo}" ha sido eliminado exitosamente.')
        return redirect('contacto_list')

    return render(request, 'contactos/contacto_confirm_delete.html', {
        'contacto': contacto
    })


# ==============================================================================
# 6. TOGGLE FAVORITO RÁPIDO
# ==============================================================================
def contacto_toggle_favorito(request, pk):
    """
    Marca o desmarca un contacto como favorito de manera instantánea.
    """
    contacto = get_object_or_404(Contacto, pk=pk)
    contacto.es_favorito = not contacto.es_favorito
    contacto.save()
    estado = "añadido a favoritos" if contacto.es_favorito else "removido de favoritos"
    messages.info(request, f'Contacto {contacto.nombre_completo} {estado}.')
    return redirect(request.META.get('HTTP_REFERER', 'contacto_list'))


# ==============================================================================
# 7. AGREGAR TELÉFONO / NOTA SECUNDARIOS
# ==============================================================================
def contacto_add_telefono(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        form = TelefonoSecundarioForm(request.POST)
        if form.is_valid():
            tel = form.save(commit=False)
            tel.contacto = contacto
            tel.save()
            messages.success(request, 'Teléfono adicional agregado exitosamente.')
        else:
            messages.error(request, 'Error al agregar el teléfono adicional.')
    return redirect('contacto_detail', pk=contacto.pk)


def contacto_delete_telefono(request, pk, tel_pk):
    tel = get_object_or_404(TelefonoSecundario, pk=tel_pk, contacto_id=pk)
    tel.delete()
    messages.success(request, 'Teléfono secundario eliminado.')
    return redirect('contacto_detail', pk=pk)


def contacto_add_nota(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.method == 'POST':
        form = NotaContactoForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.contacto = contacto
            nota.save()
            messages.success(request, 'Nota agregada a la bitácora.')
        else:
            messages.error(request, 'El título y detalle de la nota son obligatorios.')
    return redirect('contacto_detail', pk=contacto.pk)


def contacto_delete_nota(request, pk, nota_pk):
    nota = get_object_or_404(NotaContacto, pk=nota_pk, contacto_id=pk)
    nota.delete()
    messages.success(request, 'Nota eliminada de la bitácora.')
    return redirect('contacto_detail', pk=pk)


# ==============================================================================
# 8. EXPORTACIÓN CSV PÚBLICA / WEB
# ==============================================================================
def contacto_exportar_csv(request):
    """
    Descarga en CSV los contactos filtrados según la búsqueda activa.
    """
    query = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '')
    solo_favoritos = request.GET.get('favoritos', '')

    contactos = Contacto.objects.select_related('categoria').all()
    if query:
        contactos = contactos.filter(
            Q(nombre__icontains=query) | Q(apellido__icontains=query) | Q(email__icontains=query)
        )
    if categoria_id:
        contactos = contactos.filter(categoria_id=categoria_id)
    if solo_favoritos == '1':
        contactos = contactos.filter(es_favorito=True)

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="contactos_agenda.csv"'
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow(["ID", "Nombre Completo", "Email", "Teléfono", "Categoría", "Empresa", "Cargo", "Es Favorito"])
    for c in contactos:
        writer.writerow([
            c.id, c.nombre_completo, c.email, c.telefono,
            c.categoria.nombre if c.categoria else "Sin categoría",
            c.empresa or "", c.cargo or "", "Sí" if c.es_favorito else "No"
        ])
    return response


# ==============================================================================
# 9. GESTIÓN DE CATEGORÍAS (CRUD SIMPLE)
# ==============================================================================
def categoria_list(request):
    categorias = Categoria.objects.annotate(num_contactos=Count('contactos')).all()
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            cat = form.save()
            messages.success(request, f'Categoría "{cat.nombre}" creada.')
            return redirect('categoria_list')
        else:
            messages.error(request, 'Error al crear la categoría. Revisa los datos.')
    else:
        form = CategoriaForm()

    return render(request, 'contactos/categoria_list.html', {
        'categorias': categorias,
        'form': form
    })


def categoria_delete(request, pk):
    cat = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        nombre = cat.nombre
        cat.delete()
        messages.success(request, f'Categoría "{nombre}" eliminada.')
    return redirect('categoria_list')
=======
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
>>>>>>> 608b130aaff29eebc63ffd6d14385d2a72557e80
