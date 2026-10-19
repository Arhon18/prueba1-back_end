"""
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
    """
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
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
