from django.test import TestCase, Client
from django.urls import reverse
from .models import Contacto, Categoria, TelefonoSecundario, NotaContacto

class ContactoModelAndViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.categoria = Categoria.objects.create(nombre="Trabajo", color="#0284c7")
        self.contacto = Contacto.objects.create(
            nombre="Juan",
            apellido="Pérez",
            email="juan.perez@test.cl",
            telefono="+56912345678",
            categoria=self.categoria,
            empresa="Prueba SpA",
            cargo="Ingeniero",
            es_favorito=True
        )

    def test_contacto_creacion_y_propiedades(self):
        self.assertEqual(self.contacto.nombre_completo, "Juan Pérez")
        self.assertEqual(self.contacto.iniciales, "JP")
        self.assertTrue(self.contacto.es_favorito)

    def test_contacto_list_view(self):
        response = self.client.get(reverse('contacto_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Juan Pérez")
        self.assertContains(response, "juan.perez@test.cl")

    def test_contacto_search(self):
        response = self.client.get(reverse('contacto_list') + '?q=Juan')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Juan Pérez")

        response_empty = self.client.get(reverse('contacto_list') + '?q=Inexistente')
        self.assertEqual(response_empty.status_code, 200)
        self.assertNotContains(response_empty, "Juan Pérez")

    def test_contacto_create_view(self):
        data = {
            'nombre': 'Ana',
            'apellido': 'Gómez',
            'email': 'ana.gomez@test.cl',
            'telefono': '+56988776655',
            'categoria': self.categoria.id,
            'es_favorito': False,
        }
        response = self.client.post(reverse('contacto_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contacto.objects.filter(email='ana.gomez@test.cl').exists())

    def test_contacto_update_view(self):
        response = self.client.post(reverse('contacto_update', kwargs={'pk': self.contacto.pk}), {
            'nombre': 'Juan Carlos',
            'apellido': 'Pérez',
            'email': 'juan.perez@test.cl',
            'telefono': '+56912345678',
            'categoria': self.categoria.id,
            'es_favorito': True,
        })
        self.assertEqual(response.status_code, 302)
        self.contacto.refresh_from_db()
        self.assertEqual(self.contacto.nombre, 'Juan Carlos')

    def test_contacto_delete_view(self):
        response = self.client.post(reverse('contacto_delete', kwargs={'pk': self.contacto.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Contacto.objects.filter(pk=self.contacto.pk).exists())

    def test_exportar_csv(self):
        response = self.client.get(reverse('contacto_exportar_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('attachment; filename="contactos_agenda.csv"', response['Content-Disposition'])
