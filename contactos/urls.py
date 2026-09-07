"""
Rutas URL para la aplicación 'contactos'.
Arquitectura MVT de Django: Enrutamiento de peticiones a vistas.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_contactos, name='lista_contactos'),
    path('nuevo/', views.agregar_contacto, name='agregar_contacto'),
    path('contacto/<int:pk>/', views.detalle_contacto, name='detalle_contacto'),
    path('contacto/<int:pk>/editar/', views.editar_contacto, name='editar_contacto'),
    path('contacto/<int:pk>/eliminar/', views.eliminar_contacto, name='eliminar_contacto'),
]
