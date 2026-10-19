# Evaluación Sumativa 2: Programación Backend (Django)
**Asignatura:** Programación Back End (TI3041)  
**Institución:** INACAP  
**Caso desarrollado:** **Caso 3 - Agenda de Contactos Personal 2**  
**Despliegue de Producción (Vercel / PaaS):** `https://backendunidad1.vercel.app`

---

## 📌 Descripción del Proyecto
Aplicación web robusta desarrollada bajo la arquitectura **Modelo-Vista-Plantilla (MVT)** de Django para la gestión integral de contactos personales, categorización temática, control de números telefónicos secundarios, bitácora de notas y exportación masiva a formato CSV. Diseñada con interfaz responsiva, alertas interactivas, paginación, filtros avanzados y administración personalizada con branding institucional.

---

## 🎯 Cumplimiento de Criterios e Indicadores de Evaluación (Puntaje Máximo: 6 Puntos c/u)

| Indicador de Evaluación | Estado | Detalle de Implementación en el Proyecto |
| :--- | :---: | :--- |
| **1. Conexión a Base de Datos (Supabase / PaaS)** | **6 Pts** | Soporte dual en `core/settings.py` para PostgreSQL mediante variable unificada `DATABASE_URL` (Supabase Connection Pooler / Neon) o variables individuales (`host`, `port`, `database`, `user`, `password`). Ejecución limpia de migraciones (`makemigrations`, `migrate`). |
| **2. Django Admin Avanzado** | **6 Pts** | Registro personalizado de modelos (`Contacto`, `Categoria`, `TelefonoSecundario`, `NotaContacto`). Incluye **búsqueda por nombre y email**, filtros laterales (`SimpleListFilter` por cumpleaños del mes y bitácora), **inlines tabulares y apilados** (`TabularInline`, `StackedInline`), y acción masiva de **exportación a CSV**. |
| **3. CRUD Completo con Validaciones** | **6 Pts** | Operaciones Create, Read, Update y Delete completas con validación de expresiones regulares de teléfono (8 a 15 dígitos), verificación de correos duplicados, eliminación protegida con confirmación y manejo de errores con bloques try/except. |
| **4. Presentación de Resultados** | **6 Pts** | Documentación exhaustiva en README, dashboard con tarjetas métricas (total contactos, favoritos, categorías, cumpleaños del mes) e informe técnico de arquitectura y endpoints. |
| **5. Mensajes de Interfaz y Feedback UX** | **6 Pts** | Integración del framework `django.contrib.messages` para alertas de éxito, advertencia e información. Paginación en listados (Bootstrap 5) y badges visuales según la categoría del contacto. |
| **6. Variables de Entorno y Seguridad** | **6 Pts** | Uso de `python-dotenv` para cargar variables críticas (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, credenciales de BD). Archivo `.env` excluido en `.gitignore` y plantilla documentada en `.env.example`. |
| **7. Archivos Estáticos y Media** | **6 Pts** | Configuración de **WhiteNoise** (`CompressedManifestStaticFilesStorage`) en middleware y settings para servir estáticos optimizados en producción sin depender de servidores web externos. |
| **8. Despliegue en la Nube con Vercel** | **6 Pts** | Archivo `vercel.json` configurado para WSGI (`core/wsgi.py`), soporte de Serverless Functions y manejo de logs operativos a través del dashboard de Vercel. |
| **9. URL Pública y Flujo Funcional** | **6 Pts** | URL operativa accesible con flujo CRUD completo disponible para el usuario final y panel `/admin/`. |
| **10. Branding de Django Admin** | **6 Pts** | Personalización de `admin.site.site_header`, `admin.site.site_title` e `admin.site.index_title` adaptado al Caso 3 (*"Agenda Personal | Panel Administrativo"*). |

---

## 🗄️ Modelo de Datos (Caso 3: Agenda Personal)

1. **`Categoria`**:
   - Clasificación por grupos (`Trabajo`, `Familia`, `Amigos`, etc.).
   - Atributos: `nombre`, `color` (hexadecimal para badges visuales), `descripcion`.
2. **`Contacto` (Modelo Principal)**:
   - Atributos: `nombre`, `apellido`, `email` (único), `telefono` (validador regex internacional), `categoria` (FK), `empresa`, `cargo`, `fecha_nacimiento`, `es_favorito`, `direccion`, `notas`, `fecha_creacion`, `fecha_actualizacion`.
   - Propiedades calculadas: `nombre_completo`, `iniciales`, `dias_para_cumpleanos`.
3. **`TelefonoSecundario` (Relación Uno a Muchos / Inline Admin)**:
   - Permite registrar múltiples teléfonos clasificados por tipo (`móvil`, `trabajo`, `casa`, `otro`).
4. **`NotaContacto` (Bitácora Fechada / Inline Admin)**:
   - Permite registrar apuntes y notas históricas con marca de tiempo automática.

---

## 🛠️ Tecnologías Utilizadas
- **Python 3.10+ / 3.14**
- **Django 5.x / 6.x**
- **PostgreSQL / Supabase:** Motor de base de datos relacional para producción.
- **dj-database-url & psycopg2-binary:** Manejo de conexiones seguras a PostgreSQL.
- **WhiteNoise:** Servicio eficiente de archivos estáticos en entornos serverless/PaaS.
- **Bootstrap 5 & Bootstrap Icons:** Diseño responsivo, tarjetas modernas y componentes visuales.
- **python-dotenv:** Aislamiento de variables de entorno.

---

## 🚀 Guía de Instalación y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/luisduran01/backendunidad1.git
cd backendunidad1
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Copia el archivo `.env.example` y renómbralo a `.env`:
```bash
cp .env.example .env
```
*(Si dejas los campos de base de datos vacíos, el sistema usará automáticamente SQLite para desarrollo local).*

### 4. Aplicar migraciones
```bash
python manage.py migrate
```

### 5. Crear superusuario para Django Admin
```bash
python manage.py createsuperuser
```

### 6. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```
Accede a la aplicación en: `http://127.0.0.1:8000/`  
Accede al panel de administración en: `http://127.0.0.1:8000/admin/`

---

## ☁️ Instrucciones para Despliegue en Supabase y Vercel

1. **Crear Proyecto en Supabase:**
   - Crear una nueva base de datos PostgreSQL en [Supabase](https://supabase.com).
   - Obtener la URI en **Project Settings > Database > Connection String (URI / Pooler)**.
2. **Configurar Variables en Vercel:**
   - En el panel de Vercel (**Settings > Environment Variables**), agregar:
     - `SECRET_KEY`: Una cadena segura y aleatoria.
     - `DEBUG`: `False`
     - `ALLOWED_HOSTS`: `tu-app.vercel.app,.vercel.app`
     - `DATABASE_URL`: URI de conexión provista por Supabase.
3. **Ejecutar migraciones en la base de datos remota:**
   ```bash
   DATABASE_URL="tu-connection-string" python manage.py migrate
   ```
4. **Desplegar:**
   - Conectar el repositorio de GitHub con Vercel. Las compilaciones se dispararán automáticamente con cada `push` a la rama `main`.
