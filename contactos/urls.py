from django.urls import path
from . import views

urlpatterns = [
    # Contactos - CRUD principal
    path('', views.contacto_list, name='contacto_list'),
    path('contactos/nuevo/', views.contacto_create, name='contacto_create'),
    path('contactos/<int:pk>/', views.contacto_detail, name='contacto_detail'),
    path('contactos/<int:pk>/editar/', views.contacto_update, name='contacto_update'),
    path('contactos/<int:pk>/eliminar/', views.contacto_delete, name='contacto_delete'),
    path('contactos/<int:pk>/favorito/', views.contacto_toggle_favorito, name='contacto_toggle_favorito'),

    # Teléfonos adicionales y Notas (maestro-detalle)
    path('contactos/<int:pk>/telefonos/nuevo/', views.contacto_add_telefono, name='contacto_add_telefono'),
    path('contactos/<int:pk>/telefonos/<int:tel_pk>/eliminar/', views.contacto_delete_telefono, name='contacto_delete_telefono'),
    path('contactos/<int:pk>/notas/nueva/', views.contacto_add_nota, name='contacto_add_nota'),
    path('contactos/<int:pk>/notas/<int:nota_pk>/eliminar/', views.contacto_delete_nota, name='contacto_delete_nota'),

    # Exportación
    path('exportar/csv/', views.contacto_exportar_csv, name='contacto_exportar_csv'),

    # Categorías
    path('categorias/', views.categoria_list, name='categoria_list'),
    path('categorias/<int:pk>/eliminar/', views.categoria_delete, name='categoria_delete'),
]
