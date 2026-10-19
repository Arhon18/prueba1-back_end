from django import template
from django.conf import settings
from contactos.models import Contacto, NotaContacto

register = template.Library()


@register.simple_tag
def get_admin_dashboard_stats():
    """
    Retorna métricas del sistema para mostrar en el Dashboard del Django Admin.
    """
    try:
        total_contactos = Contacto.objects.count()
        total_notas = NotaContacto.objects.count()
        notas_importantes = NotaContacto.objects.filter(es_importante=True).count()
    except Exception:
        total_contactos = 0
        total_notas = 0
        notas_importantes = 0

    # Motor de base de datos actual
    db_engine = settings.DATABASES.get('default', {}).get('ENGINE', '')
    if 'postgresql' in db_engine:
        db_label = 'PostgreSQL (Producción)'
    elif 'sqlite' in db_engine:
        db_label = 'SQLite (Local)'
    else:
        db_label = 'Base de Datos'

    return {
        'total_contactos': total_contactos,
        'total_notas': total_notas,
        'notas_importantes': notas_importantes,
        'db_label': db_label,
    }
