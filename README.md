# 🏦 Sistema de Gestión de Trámites Municipales - Backend

Este repositorio contiene el núcleo lógico (Backend) del sistema de gestión de permisos y documentación legal, desarrollado con **Django** y **Django REST Framework**. El sistema está diseñado para integrarse con una base de datos MySQL estructurada y servir datos a una interfaz de usuario moderna.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.14+
* **Framework:** Django 6.0.4
* **API:** Django REST Framework (DRF)
* **Base de Datos:** MySQL / SQLite (Desarrollo)
* **Seguridad:** Python-dotenv / Variables de entorno
* **Capa de Conexión:** CORS Headers

## 🚀 Mejoras e Implementaciones Recientes

### 1. Sincronización de Modelos y DB
Se realizó un mapeo exhaustivo de los modelos de Django para coincidir exactamente con el diseño físico de la base de datos de ingeniería.
* Implementación de `db_table` y `db_column` para asegurar compatibilidad con tablas existentes.
* Estandarización de nombres de campos (ej. `id_documento`, `id_cliente`).

### 2. Capa de Seguridad (Ciberseguridad)
Siguiendo mejores prácticas de seguridad informática:
* **Variables de Entorno:** Se configuró el `settings.py` para utilizar variables de entorno para la `SECRET_KEY`, credenciales de base de datos y configuración de correos, evitando la exposición de datos sensibles en el repositorio público.
* **CORS Policy:** Implementación de `django-cors-headers` para permitir la comunicación segura con el frontend.
* **Admin Protegido:** Registro de usuarios mediante `UserAdmin` para una gestión jerárquica y segura de accesos.

### 3. Gestión de Archivos (Media)
* Configuración de `MEDIA_ROOT` y `MEDIA_URL` para el manejo de archivos físicos (PDFs, imágenes de trámites).
* Sincronización de rutas en `urls.py` para permitir la previsualización de documentos desde el navegador en entornos de desarrollo.

### 4. Panel de Administración Avanzado
* Personalización de la interfaz `django-admin` para visualización de documentos, logs de auditoría y estados de trámites en tiempo real.
* Configuración de campos de solo lectura (`readonly_fields`) para los registros de historial y logs para garantizar la integridad de la auditoría.

## 📂 Estructura del Proyecto
* `/gestion_clientes`: Aplicación principal con la lógica de negocio.
* `/mi_proyecto`: Configuración global, seguridad y rutas.
* `/media`: Directorio local para almacenamiento de documentos subidos (ignorado en Git por seguridad).
* `/docs_base_datos`: Documentación técnica y diagramas SQL.

## ⚙️ Configuración Local
1. Clonar el repositorio.
2. Crear un entorno virtual: `python -m venv env`.
3. Instalar dependencias: `pip install -r requirements.txt`.
4. Configurar variables de entorno en un archivo `.env`.
5. Ejecutar migraciones: `python manage.py migrate`.
6. Iniciar servidor: `python manage.py runserver`.

---
**Desarrollado por el equipo de Ingeniería en Sistemas - Tecnológico de Tijuana (2026)**
