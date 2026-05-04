from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 
from .models import (
    Usuario, Cliente, TipoDocumento, EstadoDocumento, 
    Documento, Notificacion, Log, HistorialDocumento, ConfiguracionAlerta
)

# 1. Registros Simples (Catálogos)
admin.site.register(Usuario,UserAdmin)
admin.site.register(Cliente)
admin.site.register(TipoDocumento)
admin.site.register(EstadoDocumento)
admin.site.register(Notificacion)
admin.site.register(ConfiguracionAlerta)

# 2. Registro Avanzado de Documentos
@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    # CAMBIO: 'id' ahora es 'id_documento'
    list_display = ('id_documento', 'cliente', 'tipo', 'estado', 'fecha_vencimiento', 'creado_en')
    list_filter = ('estado', 'tipo', 'creado_en')
    search_fields = ('cliente__nombre', 'nombre_archivo')

# 3. Registro Protegido de Logs (Solo lectura)
@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    # CAMBIO: 'tabla_affected' ahora es 'tabla_afectada'
    list_display = ('fecha', 'usuario', 'accion', 'tabla_afectada')
    readonly_fields = ('fecha', 'usuario', 'accion', 'tabla_afectada', 'id_registro')

# 4. Registro de Historial de Cambios
@admin.register(HistorialDocumento)
class HistorialAdmin(admin.ModelAdmin):
    # CAMBIO: 'id_historial' es opcional aquí, pero los campos internos deben existir en el modelo
    list_display = ('documento', 'estado_anterior', 'estado_nuevo', 'fecha_cambio', 'usuario')
    readonly_fields = ('fecha_cambio',)