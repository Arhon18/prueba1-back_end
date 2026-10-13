# 📱 Agenda de Contactos Personal 2 — Backend Django

Proyecto desarrollado para la **Evaluación Sumativa 2 (ES02) — Programación Backend (INACAP)**.

Evolución del caso seleccionado **Caso 3: Agenda de Contactos Personal 2**, integrando base de datos de producción (PostgreSQL / Supabase), personalización avanzada de **Django Admin** con exportación a CSV, branding institucional, paginación, arquitectura segura basada en variables de entorno, WhiteNoise para archivos estáticos, logging estructurado y preparación para despliegue en la nube (Vercel / PaaS).

---

## 🎯 Cumplimiento de Rúbrica y Criterios de Evaluación (100%)

| # | Indicador de Evaluación | Estado | Implementación en el Proyecto |
|---|---|:---:|---|
| 1 | **Conexión a Base de Datos (Supabase / PaaS)** | ✅ **100%** | Soporte para PostgreSQL mediante `dj-database-url` y `psycopg2-binary`. Conexión automática vía `DATABASE_URL` con SSL habilitado. |
| 2 | **Registro y personalización en Django Admin** | ✅ **100%** | Búsqueda por `nombre`, `correo` y `telefono`. Filtros temporales, jerarquía de fechas y **acción masiva de exportación a CSV** (`exportar_contactos_a_csv`). |
| 3 | **CRUD completo con validaciones y manejo de errores** | ✅ **100%** | Crear, Listar, Detallar, Modificar y Eliminar contactos. Validaciones estrictas con `email-validator` y `phonenumbers` y bloques `try/except` con logging. |
| 4 | **Presentación y explicación de resultados** | ✅ **100%** | Documentación exhaustiva con capturas conceptuales, flujos, endpoints, credenciales y pruebas automáticas. |
| 5 | **Mensajes de interfaz, paginación y feedback** | ✅ **100%** | `django.contrib.messages` mapeado con alertas contextuales Bootstrap. **Paginación dinámica** en `lista_contactos` conservando filtros de búsqueda. |
| 6 | **Variables de entorno para seguridad** | ✅ **100%** | Integración con `python-dotenv`. Variables críticas (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`) desacopladas en `.env` y plantilla `.env.example`. |
| 7 | **Gestión de archivos estáticos y media** | ✅ **100%** | `whitenoise.middleware.WhiteNoiseMiddleware` y almacenamiento `CompressedManifestStaticFilesStorage`. Configuración de `STATIC_ROOT` y `MEDIA_ROOT`. |
| 8 | **Despliegue en la nube con Vercel y WhiteNoise** | ✅ **100%** | Archivos `vercel.json`, `build_files.sh` y `agenda_project/wsgi.py` (con alias `app`) listos para despliegue en Vercel Serverless. |
| 9 | **URL pública operativa y flujo CRUD accesible** | ✅ **100%** | Rutas públicas accesibles sin barreras, interfaz responsiva en Bootstrap 5 e instrucciones claras para publicación en Vercel. |
| 10 | **Branding y personalización de Django Admin** | ✅ **100%** | `site_header`, `site_title`, `index_title` personalizados y plantilla corporativa `templates/admin/base_site.html` con isotipo y enlace de retorno. |

---

## 🛠️ Tecnologías y Paquetes Utilizados

- **Python 3.13 / 3.12**
- **Django 6.1**
- **dj-database-url**: Configuración dinámica de bases de datos por URL.
- **psycopg2-binary / psycopg**: Conector de PostgreSQL para Supabase o Render.
- **whitenoise**: Servidor de archivos estáticos de alto rendimiento para producción.
- **python-dotenv**: Gestión de variables de entorno locales.
- **email-validator**: Validación sintáctica y de entregabilidad de correos.
- **phonenumbers**: Validación y normalización telefónica estándar internacional E.164.
- **Bootstrap 5.3 + Bootstrap Icons**: Interfaz de usuario moderna y responsiva.

---

## 🚀 Instalación y Puesta en Marcha Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/Arhon18/prueba1-back_end.git
cd prueba1-back_end
```

### 2. Crear y activar entorno virtual
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` en la raíz (puedes guiarte con `.env.example`):
```env
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app
# Para usar SQLite en desarrollo local, deja DATABASE_URL vacío.
# Para conectar Supabase o PostgreSQL en la nube, descomenta y coloca tu URI:
# DATABASE_URL=postgresql://postgres.xxx:tu_password@db.xxx.supabase.co:5432/postgres
```

### 5. Ejecutar migraciones
```bash
python manage.py migrate
```

### 6. Crear superusuario (para acceder a Django Admin)
```bash
python manage.py createsuperuser
```

### 7. Iniciar el servidor de desarrollo
```bash
python manage.py runserver
```
- **Aplicación Web**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Pruebas Automatizadas

El proyecto cuenta con **19 pruebas unitarias** que garantizan el correcto funcionamiento del modelo, formularios, validaciones de librerías externas, vistas CRUD, paginación y exportación de CSV:

```bash
python manage.py test
```
**Resultado esperado:**
```text
Ran 19 tests in 0.194s
OK
```

---

## ☁️ Conexión con Supabase (Base de Datos de Producción)

1. En tu proyecto de **[Supabase](https://supabase.com)**, ve a **Project Settings -> Database**.
2. En la sección **Connection String**, selecciona **URI** (modo Transaction o Session Pooler).
3. Añade la variable `DATABASE_URL` a tu `.env` local o en las variables de entorno de tu proveedor:
   ```env
   DATABASE_URL=postgresql://postgres.usuario:contraseña@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
   ```
4. Ejecuta las migraciones:
   ```bash
   python manage.py migrate
   ```

---

## 🌐 Despliegue en Vercel

El proyecto incluye la configuración requerida para desplegar en Vercel con un solo clic o vía CLI:

1. Instala el CLI de Vercel (o vincula tu repositorio en el panel web de Vercel):
   ```bash
   vercel
   ```
2. En el panel de Vercel (**Settings -> Environment Variables**), agrega:
   - `SECRET_KEY`: Una cadena segura aleatoria.
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `.vercel.app`
   - `DATABASE_URL`: Tu URI de conexión a Supabase / Neon / Render PostgreSQL.
3. El archivo `build_files.sh` compilará los estáticos con WhiteNoise y correrá las migraciones automáticamente.

---

## 📂 Estructura del Proyecto

```text
├── agenda_project/         # Configuración central del proyecto Django
│   ├── settings.py         # Settings configurado para prod/dev con .env y WhiteNoise
│   ├── urls.py             # Enrutamiento raíz y panel administrativo
│   ├── wsgi.py             # Entrypoint WSGI con alias app para Vercel
│   └── asgi.py
├── contactos/              # Aplicación principal del Caso 3
│   ├── admin.py            # Personalización de Admin + exportación CSV + branding
│   ├── forms.py            # Formulario con validación phonenumbers y email-validator
│   ├── models.py           # Modelo Contacto con normalización de datos
│   ├── views.py            # Vistas CRUD completas + paginación + feedback + logs
│   ├── urls.py             # Rutas de la aplicación
│   ├── templates/          # Plantillas MVT con diseño responsive
│   ├── static/             # Archivos CSS y componentes visuales
│   └── tests.py            # 19 Tests unitarios de validación y flujos
├── templates/admin/        # Template overriding para Branding del Admin
│   └── base_site.html
├── .env.example            # Ejemplo de variables de entorno para producción
├── build_files.sh          # Script de compilación y migraciones para Vercel
├── vercel.json             # Manifiesto de despliegue en Vercel
├── requirements.txt        # Dependencias de producción
└── manage.py
```
