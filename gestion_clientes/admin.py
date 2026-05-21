from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Cliente, Documento, TipoDocumento, 
    EstadoDocumento, ReporteGenerado
)

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    model = Usuario

    list_display = (
        'username',
        'nombre',
        'rol',
        'email',
        'is_staff'
    )

    search_fields = (
        'username',
        'nombre',
        'email'
    )

    fieldsets = UserAdmin.fieldsets + (

        ('Información Extra', {
            'fields': (
                'nombre',
                'rol'
            )
        }),

    )

    add_fieldsets = UserAdmin.add_fieldsets + (

        ('Información Extra', {
            'fields': (
                'nombre',
                'rol'
            )
        }),

    )

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id_cliente', 'nombre', 'email', 'telefono')
    search_fields = ('nombre',)

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_tipo')

@admin.register(EstadoDocumento)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'color')

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('id_documento', 'cliente', 'tipo', 'estado', 'fecha_vencimiento')
    list_filter = ('estado', 'tipo', 'cliente')

@admin.register(ReporteGenerado)
class ReporteAdmin(admin.ModelAdmin):
    # Mostramos los campos nuevos que agregamos para tu tabla
    list_display = ('id_reporte', 'cliente', 'tipo_tramite', 'estatus_doc', 'usuario_creador', 'fecha_creacion')
    readonly_fields = ('fecha_creacion',)
    list_filter = ('tipo_tramite', 'estatus_doc')