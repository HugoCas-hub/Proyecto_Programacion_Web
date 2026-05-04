from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField 

# 1. USUARIOS (Primero, porque otros lo referencian)
class Usuario(AbstractUser):
    ROLES = (('admin', 'Administrador'), ('empleado', 'Empleado'))
    rol = models.CharField(max_length=10, choices=ROLES, default='empleado')

# 2. CATÁLOGOS BASE (Sin dependencias)
class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.nombre

class TipoDocumento(models.Model):
    nombre_tipo = models.CharField(max_length=100)
    def __str__(self): return self.nombre_tipo

class EstadoDocumento(models.Model):
    nombre_estado = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    def __str__(self): return self.nombre_estado

# 3. CONFIGURACIÓN Y DOCUMENTOS (Dependen de los de arriba)
class ConfiguracionAlerta(models.Model):
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    dias_rojo = models.IntegerField()
    dias_amarillo = models.IntegerField()
    activo = models.BooleanField(default=True)

class Documento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoDocumento, on_delete=models.PROTECT)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    notas = models.TextField(null=True, blank=True)
    fecha_detencion = models.DateField(null=True, blank=True)
    archivo = models.FileField(upload_to='documentos/%Y/%m/', null=True, blank=True)
    nombre_archivo = models.CharField(max_length=255, blank=True)
    tipo_mime = models.CharField(max_length=100, blank=True)
    tamano = models.IntegerField(null=True, blank=True)
    creado_por = models.ForeignKey(Usuario, related_name='docs_creados', on_delete=models.SET_NULL, null=True)
    modificado_por = models.ForeignKey(Usuario, related_name='docs_editados', on_delete=models.SET_NULL, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

# 4. AUDITORÍA Y OTROS
class HistorialDocumento(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    estado_anterior = models.CharField(max_length=50)
    estado_nuevo = models.CharField(max_length=50)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    comentario = models.TextField(null=True, blank=True)

class Log(models.Model):
    accion = models.CharField(max_length=100)
    tabla_affected = models.CharField(max_length=50)
    id_registro = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)

class Reporte(models.Model):
    tipo_reporte = models.CharField(max_length=100)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    generado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    parametros = JSONField()

class Notificacion(models.Model):
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=50)
    enviado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)