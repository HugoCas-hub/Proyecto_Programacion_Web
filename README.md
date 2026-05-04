# Sistema de Gestión de Trámites Municipales - Backend

Este es el backend del sistema desarrollado en **Django 6.0** y **Django REST Framework**. Incluye la lógica de base de datos, sistema de auditoría (logs) y notificaciones.

## 🚀 Lo que se implementó:
- **Base de Datos:** Modelos para Clientes, Documentos, Tipos de Trámite y Estados.
- **API REST:** Endpoint listo en `/api/documentos/` para el frontend.
- **Sistema de Semáforo:** Los documentos incluyen un campo `color_estado` basado en la vigencia.
- **Panel de Admin:** Configurado para gestionar catálogos y ver historial de cambios.
- **Auditoría:** Tablas de Logs e Historial para rastrear movimientos.

## 🛠️ Instalación para el equipo:
1. Clonar el repositorio.
2. Crear entorno virtual: `python -m venv env`
3. Activar entorno: `source env/Scripts/activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Aplicar migraciones: `python manage.py migrate`
6. Iniciar servidor: `python manage.py runserver`

## 🔗 Endpoints útiles:
- **API de Documentos:** http://127.0.0.1:8000/api/documentos/
- **Panel de Administración:** http://127.0.0.1:8000/admin/
