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

    def test_telefono_chileno_con_prefijo(self):
        """Verifica que un número chileno con +56 sea aceptado y validado."""
        datos = {
            'nombre': 'Martín Silva',
            'telefono': '+56 9 8765 4321',
            'correo': 'martin.silva@dominio.cl',
            'direccion': 'Calle Las Flores 123, Providencia'
        }
        form = ContactoForm(data=datos)
        self.assertTrue(form.is_valid(), f"Errores: {form.errors}")
        self.assertEqual(form.cleaned_data['telefono'], '+56 9 8765 4321')

    def test_telefono_chileno_sin_prefijo_se_normaliza(self):
        """Verifica que un número chileno de 9 dígitos sin +56 sea aceptado y normalizado con +56."""
        datos = {
            'nombre': 'Martín Silva',
            'telefono': '987654321',
            'correo': 'martin.silva@dominio.cl',
            'direccion': 'Calle Las Flores 123, Providencia'
        }
        form = ContactoForm(data=datos)
        self.assertTrue(form.is_valid(), f"Errores: {form.errors}")
        # Comprobar que se guardó normalizado con el prefijo chileno +56
        self.assertEqual(form.cleaned_data['telefono'], '+56 9 8765 4321')

    def test_telefono_extranjero_con_prefijo_valido(self):
        """Verifica que números extranjeros con '+' y código de país válido sean aceptados."""
        telefonos_extranjeros = [
            '+1 415 555 2671',      # Estados Unidos
            '+34 612 345 678',      # España
            '+54 9 11 2345 6789',   # Argentina
        ]
        for tel in telefonos_extranjeros:
            with self.subTest(telefono=tel):
                datos = {
                    'nombre': 'Contacto Extranjero',
                    'telefono': tel,
                    'correo': 'extranjero@dominio.com',
                    'direccion': 'Calle Internacional 99'
                }
                form = ContactoForm(data=datos)
                self.assertTrue(form.is_valid(), f"Error con {tel}: {form.errors}")
                self.assertTrue(form.cleaned_data['telefono'].startswith('+'))

    def test_telefono_extranjero_sin_prefijo_es_rechazado(self):
        """Verifica que un número extranjero sin '+' sea rechazado estrictamente."""
        telefonos_sin_mas = [
            '14155552671',  # EE.UU. sin '+'
            '34612345678',  # España sin '+'
            '5491123456789' # Argentina sin '+'
        ]
        for tel in telefonos_sin_mas:
            with self.subTest(telefono=tel):
                datos = {
                    'nombre': 'Contacto Prueba',
                    'telefono': tel,
                    'correo': 'prueba@dominio.com',
                    'direccion': 'Calle Principal 100'
                }
                form = ContactoForm(data=datos)
                self.assertFalse(form.is_valid(), f"El número extranjero {tel} debió ser rechazado por no llevar '+'")
                self.assertIn('telefono', form.errors)

    def test_telefono_invalido_caracteres_o_incompleto(self):
        """Verifica el rechazo de teléfonos con letras o secuencias inválidas."""
        telefonos_malos = ['abcde', '12345', '+999 000 000', '++569123']
        for tel_malo in telefonos_malos:
            with self.subTest(telefono=tel_malo):
                datos = {
                    'nombre': 'Contacto Invalido',
                    'telefono': tel_malo,
                    'correo': 'invalido@correo.cl',
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

    def test_paginacion_contactos(self):
        """Verifica el funcionamiento de la paginación con más de 6 contactos."""
        for i in range(10):
            Contacto.objects.create(
                nombre=f"Contacto Extra {i}",
                telefono=f"+56 9 1000 000{i}",
                correo=f"extra{i}@test.com",
                direccion=f"Calle Falsa {i}"
            )
        response = self.client.get(reverse('lista_contactos'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)
        self.assertEqual(len(response.context['contactos']), 6)
        self.assertTrue(response.context['page_obj'].has_next())

    def test_exportacion_csv_admin_action(self):
        """Verifica que la acción de exportación a CSV en admin retorne un archivo CSV válido."""
        from contactos.admin import exportar_contactos_a_csv
        queryset = Contacto.objects.all()
        response = exportar_contactos_a_csv(None, None, queryset)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8-sig')
        self.assertIn('attachment; filename="contactos_agenda.csv"', response['Content-Disposition'])
        contenido = response.content.decode('utf-8-sig')
        self.assertIn('Tulio Triviño', contenido)
        self.assertIn('tulio@titirilquen.cl', contenido)

    def test_admin_dashboard_stats_templatetag(self):
        """Verifica que el templatetag get_admin_dashboard_stats devuelva el conteo real de datos."""
        from contactos.templatetags.admin_dashboard_tags import get_admin_dashboard_stats
        from contactos.models import NotaContacto
        NotaContacto.objects.create(
            contacto=self.contacto1,
            titulo="Reunión Importante",
            contenido="Preparar pauta",
            es_importante=True
        )
        stats = get_admin_dashboard_stats()
        self.assertEqual(stats['total_contactos'], 3)
        self.assertEqual(stats['total_notas'], 1)
        self.assertEqual(stats['notas_importantes'], 1)
        self.assertIn('db_label', stats)

        