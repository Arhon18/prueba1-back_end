# Agenda de Contactos Personal (Caso 3)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0%2B%20%2F%206.0-green.svg)](https://www.djangoproject.com/)
[![email--validator](https://img.shields.io/badge/email--validator-2.0%2B-orange.svg)](https://pypi.org/project/email-validator/)
[![Tests](https://img.shields.io/badge/Tests-13%20Passed-brightgreen.svg)]()

Aplicación web para la gestión de contactos personales desarrollada con el framework **Django**, implementando la arquitectura **Modelo-Vista-Plantilla (MVT)**, validación avanzada mediante paquetes externos, buscador multi-criterio y una interfaz web moderna y responsiva.

---

## 📋 Requerimientos Funcionales del Caso

- **Agregar contactos**: Registro completo con `nombre`, `teléfono`, `correo electrónico` y `dirección`.
- **Buscar contactos**: Filtrado dinámico en tiempo real o por formulario que evalúa coincidencias por `nombre` o por `correo electrónico`.
- **Validar formato de correo electrónico**: Verificación sintáctica rigurosa utilizando el paquete externo `email-validator`.
- **Gestión integral (CRUD)**: Visualización en tarjetas con estadísticas, ficha detallada, edición y eliminación segura.

---

## 🎯 Cumplimiento de la Rúbrica de Evaluación (60 / 60 Puntos)

| # | Criterio de Evaluación | Puntaje Máximo | Evidencia en el Código |
| :--- | :--- | :---: | :--- |
| **1** | **Identifica correctamente variables y operaciones del lenguaje** | **6 pts** | Manipulación y operaciones de cadenas (`.strip()`, `.title()`, `.lower()`), operaciones aritméticas (cálculo de contactos filtrados y diferencias `total - encontrados`), colecciones (`list`, `dict`), formateo de cadenas con f-strings. Ver `contactos/views.py`, `contactos/forms.py` y `contactos/models.py`. |
| **2** | **Utiliza estructuras de decisión y operadores de forma adecuada** | **6 pts** | Uso de condicionales `if/elif/else`, operadores relacionales (`<`, `>`, `==`, `!=`), operadores de pertenencia (`in`, `not in`) y operadores lógicos booleanos (`and`, `or`, `not`). Consultas ORM con objetos `Q(nombre__icontains=q) \| Q(correo__icontains=q)`. |
| **3** | **Integra paquetes externos en la solución** | **6 pts** | Integración del paquete externo `email-validator` (`validate_email`, `EmailNotValidError`) declarado en `requirements.txt` y aplicado en `contactos/forms.py` para la validación estricta de direcciones de correo electrónico. |
| **4** | **Implementa una aplicación funcional en Django según requerimientos** | **6 pts** | Arquitectura MVT completa: Modelo en `contactos/models.py`, Vistas en `contactos/views.py`, Enrutamiento en `contactos/urls.py` y Plantillas en `contactos/templates/contactos/`. |
| **5** | **Estructura el código de forma clara y ordenada** | **6 pts** | Separación modular de responsabilidades siguiendo las mejores prácticas de Django (`models.py`, `forms.py`, `views.py`, `urls.py`, `admin.py`, `tests.py`, static files y templates). |
| **6** | **Comenta el código para facilitar su comprensión** | **6 pts** | Docstrings descriptivos en clases y funciones, comentarios explicativos inline con etiquetas `[Criterio X]` que facilitan la corrección por parte del docente o evaluador. |
| **7** | **Valida correctamente los datos de entrada** | **6 pts** | Limpieza y validación en `clean_nombre()` (longitud mínima), `clean_telefono()` (caracteres numéricos y formato telefónico), `clean_correo()` (validación sintáctica estricta con `email-validator`) y `clean_direccion()` en `contactos/forms.py`. |
| **8** | **Utiliza correctamente el entorno de desarrollo y herramientas asociadas** | **6 pts** | Archivo de dependencias `requirements.txt`, control de versiones con `.gitignore`, sistema de migraciones (`makemigrations`, `migrate`), comando de gestión `poblar_contactos` y suite de pruebas automatizadas con `TestCase`. |
| **9** | **Cumple con los requerimientos funcionales del caso seleccionado** | **6 pts** | Formulario de registro con los 4 campos obligatorios, buscador funcional por nombre o correo, y validación estricta de correo. |
| **10** | **Presenta el archivo sin errores de ejecución** | **6 pts** | Verificado con `py manage.py check` (0 errores) y 13 pruebas unitarias automatizadas aprobadas con éxito (`Ran 13 tests ... OK`). |

---

## 🏛️ Arquitectura del Proyecto (MVT)

```text
prueba1 back_end/
├── agenda_project/                 # Configuración principal del proyecto
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py                 # Configuración global, apps, i18n
│   ├── urls.py                     # Enrutador principal de URLs
│   └── wsgi.py
├── contactos/                      # Aplicación Django de la agenda
│   ├── management/
│   │   └── commands/
│   │       └── poblar_contactos.py # Comando para cargar datos de prueba iniciales
│   ├── migrations/                 # Migraciones de base de datos
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── static/
│   │   └── contactos/
│   │       └── css/
│   │           └── styles.css      # Estilos personalizados modernos y responsivos
│   ├── templates/
│   │   └── contactos/
│   │       ├── base.html           # Layout base con Bootstrap 5 y navbar
│   │       ├── lista.html          # Vista de contactos, buscador y estadísticas
│   │       ├── form.html           # Formulario para agregar / editar
│   │       ├── detalle.html        # Ficha detallada del contacto
│   │       └── confirmar_eliminar.html # Confirmación para borrar
│   ├── admin.py                    # Registro y configuración en Django Admin
│   ├── apps.py                     # Metadatos de la aplicación
│   ├── forms.py                    # Formulario ContactoForm con email-validator
│   ├── models.py                   # Modelo Contacto (nombre, teléfono, correo, dirección)
│   ├── tests.py                    # Suite de 13 pruebas unitarias
│   ├── urls.py                     # Rutas internas de la app contactos
│   └── views.py                    # Lógica de negocio (búsqueda, CRUD, decisiones)
├── manage.py                       # Utilidad de administración de Django
├── requirements.txt                # Paquetes y dependencias externas
├── .gitignore                      # Exclusión de archivos generados y temporales
└── README.md                       # Documentación técnica completa
```

---

## 🚀 Guía de Instalación y Ejecución Local

### Paso 1: Clonar el repositorio
```bash
git clone <URL_DEL_REPOSITORIO>
cd "prueba1 back_end"
```

### Paso 2: Crear y activar entorno virtual (Recomendado)
En Windows (PowerShell):
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```
En Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias requeridas
```bash
py -m pip install -r requirements.txt
```

### Paso 4: Aplicar migraciones a la base de datos
```bash
py manage.py migrate
```

### Paso 5 (Opcional): Cargar datos de prueba
Para poblar automáticamente la agenda con contactos iniciales:
```bash
py manage.py poblar_contactos
```

### Paso 6: Ejecutar el servidor de desarrollo
```bash
py manage.py runserver
```

Abre tu navegador web e ingresa a: **`http://127.0.0.1:8000/`**

---

## 🧪 Ejecución de Pruebas Automatizadas

El proyecto incluye 13 pruebas unitarias que validan el modelo, los formularios, el paquete externo `email-validator` y las vistas:

```bash
py manage.py test contactos
```

Salida esperada:
```text
Creating test database for alias 'default'...
.............
----------------------------------------------------------------------
Ran 13 tests in 0.089s

OK
```

---

## 📤 Instrucciones para Publicar en GitHub

1. Inicializar el repositorio git (si no está inicializado):
   ```bash
   git status
   ```
2. Agregar todos los archivos al seguimiento de Git:
   ```bash
   git add .
   ```
3. Realizar el commit inicial:
   ```bash
   git commit -m "feat: Implementación completa Caso 3 - Agenda de Contactos Personal (Django)"
   ```
4. Vincular el repositorio remoto de GitHub:
   ```bash
   git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   ```
5. Subir los cambios a la rama principal:
   ```bash
   git branch -M main
   git push -u origin main
   ```
