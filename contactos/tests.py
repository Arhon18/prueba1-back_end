"""
Suite de Pruebas Unitarias para la Agenda de Contactos.

"""

from django.test import TestCase, Client
from django.urls import reverse
from contactos.models import Contacto
from contactos.forms import ContactoForm


class ContactoModelTest(TestCase):
    """
    Pruebas unitarias para el modelo Contacto.
    """

    def setUp(self):
        self.contacto = Contacto.objects.create(
            nombre="Valentina Ríos",
            telefono="+56 9 1122 3344",
            correo="valentina.rios@ejemplo.cl",
            direccion="Av. Apoquindo 4000, Las Condes"
        )

    def test_creacion_contacto(self):
        """Verifica que el contacto se cree con los campos correctos."""
        self.assertEqual(self.contacto.nombre, "Valentina Ríos")
        self.assertEqual(self.contacto.telefono, "+56 9 1122 3344")
        self.assertEqual(self.contacto.correo, "valentina.rios@ejemplo.cl")
        self.assertEqual(self.contacto.direccion, "Av. Apoquindo 4000, Las Condes")
        self.assertTrue(self.contacto.fecha_creacion is not None)

    def test_str_representacion(self):
        """Verifica la representación legible __str__ del modelo."""
        esperado = "Valentina Ríos (valentina.rios@ejemplo.cl)"
        self.assertEqual(str(self.contacto), esperado)


class ContactoFormValidationTest(TestCase):
    """
    Pruebas de validación de datos de entrada y paquete externo 'email-validator'.
    Requerimiento: 'Validar formato de correo electrónico'.
    """

    def test_correo_valido_con_paquete_externo(self):
        """Verifica que un correo con formato válido sea aceptado por email-validator."""
        datos = {
            'nombre': 'Martín Silva',
            'telefono': '+56 9 9988 7766',
            'correo': 'martin.silva@dominio.com',
            'direccion': 'Calle Las Flores 123, Providencia'
        }
        form = ContactoForm(data=datos)
        self.assertTrue(form.is_valid(), f"Errores encontrados: {form.errors}")

    def test_correo_invalido_rechazado_por_validador(self):
        """Verifica que correos con sintaxis inválida sean rechazados."""
        correos_invalidos = [
            'correo_sin_arroba.com',
            'usuario@',
            '@dominio.com',
            'usuario@@doblearroba.com',
            'usuario con espacios@dominio.com',
        ]
        for correo_malo in correos_invalidos:
            with self.subTest(correo=correo_malo):
                datos = {
                    'nombre': 'Martín Silva',
                    'telefono': '+56 9 9988 7766',
                    'correo': correo_malo,
                    'direccion': 'Calle Las Flores 123, Providencia'
                }
                form = ContactoForm(data=datos)
                self.assertFalse(form.is_valid(), f"El correo '{correo_malo}' debió ser rechazado.")
                self.assertIn('correo', form.errors)

    def test_nombre_demasiado_corto(self):
        """Verifica que un nombre con menos de 3 caracteres sea rechazado."""
        datos = {
            'nombre': 'Al',
            'telefono': '+56 9 9988 7766',
            'correo': 'valido@correo.cl',
            'direccion': 'Calle Principal 100'
        }
        form = ContactoForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_telefono_caracteres_invalidos(self):
        """Verifica que caracteres no numéricos prohibidos en teléfono sean rechazados."""
        datos = {
            'nombre': 'Martín Silva',
            'telefono': 'telefono_invalido_abc',
            'correo': 'valido@correo.cl',
            'direccion': 'Calle Principal 100'
        }
        form = ContactoForm(data=datos)
        self.assertFalse(form.is_valid())
        self.assertIn('telefono', form.errors)


class ContactoViewsTest(TestCase):
    """
    Pruebas de vistas, controladores y requerimiento de búsqueda.
    Requerimientos:
    Buscar contactos por nombre o correo
    Agregar contactos con nombre, teléfono, correo y dirección

    """

    def setUp(self):
        self.client = Client()
        self.contacto1 = Contacto.objects.create(
            nombre="Juan Carlos Bodoque",
            telefono="+56 9 1234 5678",
            correo="bodoque@titirilquen.cl",
            direccion="Estudios Centrales de TV"
        )
        self.contacto2 = Contacto.objects.create(
            nombre="Tulio Triviño",
            telefono="+56 9 8765 4321",
            correo="tulio@titirilquen.cl",
            direccion="Mansión Triviño, Titirilquén"
        )
        self.contacto3 = Contacto.objects.create(
            nombre="Patana Tufillo",
            telefono="+56 9 5555 4444",
            correo="patana@periodismo.cl",
            direccion="Calle de las Rosas 55"
        )

    def test_vista_lista_contactos_status_code(self):
        """Verifica que la página principal responda HTTP 200."""
        response = self.client.get(reverse('lista_contactos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contactos/lista.html')
        self.assertEqual(len(response.context['contactos']), 3)

    def test_busqueda_por_nombre(self):
        """Verifica la búsqueda por coincidencia en el nombre."""
        response = self.client.get(reverse('lista_contactos'), {'q': 'Bodoque'})
        self.assertEqual(response.status_code, 200)
        contactos_resultado = list(response.context['contactos'])
        self.assertEqual(len(contactos_resultado), 1)
        self.assertEqual(contactos_resultado[0].nombre, "Juan Carlos Bodoque")

    def test_busqueda_por_correo(self):
        """Verifica la búsqueda por coincidencia en el correo."""
        response = self.client.get(reverse('lista_contactos'), {'q': 'periodismo.cl'})
        self.assertEqual(response.status_code, 200)
        contactos_resultado = list(response.context['contactos'])
        self.assertEqual(len(contactos_resultado), 1)
        self.assertEqual(contactos_resultado[0].nombre, "Patana Tufillo")

    def test_busqueda_sin_resultados(self):
        """Verifica el comportamiento cuando la búsqueda no coincide."""
        response = self.client.get(reverse('lista_contactos'), {'q': 'InexistenteXYZ'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['contactos']), 0)
        self.assertContains(response, "No se encontraron resultados")

    def test_agregar_contacto_post_exitoso(self):
        """Verifica el flujo completo de agregar un nuevo contacto."""
        datos_nuevo = {
            'nombre': 'Policarpo Avendaño',
            'telefono': '+56 9 3333 2222',
            'correo': 'policarpo@rankingtop.cl',
            'direccion': 'Plaza Central 12'
        }
        response = self.client.post(reverse('agregar_contacto'), data=datos_nuevo)
        # Debe redirigir a la lista
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('lista_contactos'))
        # Comprobar que existe en base de datos
        self.assertTrue(Contacto.objects.filter(correo='policarpo@rankingtop.cl').exists())

    def test_detalle_contacto(self):
        """Verifica que la vista de detalle cargue correctamente."""
        response = self.client.get(reverse('detalle_contacto', kwargs={'pk': self.contacto1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.contacto1.nombre)
        self.assertContains(response, self.contacto1.correo)

    def test_eliminar_contacto(self):
        """Verifica la eliminación segura de un contacto mediante POST."""
        contacto_id = self.contacto3.pk
        response = self.client.post(reverse('eliminar_contacto', kwargs={'pk': contacto_id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Contacto.objects.filter(pk=contacto_id).exists())
        