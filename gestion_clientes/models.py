from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=50, choices=[('admin', 'Administrador'), ('empleado', 'Empleado')])

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    def __str__(self): return self.nombre

class TipoDocumento(models.Model):
    nombre_tipo = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nombre_tipo

class EstadoDocumento(models.Model):

    OPCIONES_COLOR = [
        ('gris', '⚪ Gris'),
        ('verde', '🟢 Verde'),
        ('amarillo', '🟡 Amarillo'),
        ('rojo', '🔴 Rojo'),
    ]

    nombre = models.CharField(
        max_length=50,
        unique=True
    )

    color = models.CharField(
        max_length=20,
        choices=OPCIONES_COLOR,
        default='gris',
        blank=True
    )

    def __str__(self):
        return self.nombre

class Documento(models.Model):
    id_documento = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='documentos')
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT)
    estado = models.ForeignKey(EstadoDocumento, on_delete=models.PROTECT)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    archivo = models.FileField(upload_to='documentos/', null=True, blank=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    @property
    def semaforo_color(self):
        if not self.fecha_vencimiento: return "gris"
        hoy = timezone.now().date()
        dias = (self.fecha_vencimiento - hoy).days
        if dias <= 0: return "rojo"
        if dias <= 30: return "amarillo"
        return "verde"
    
    def __str__(self):
        return f"{self.cliente.nombre} - {self.tipo.nombre_tipo} - {self.estado.nombre}"  

class ReporteGenerado(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente,on_delete=models.PROTECT,null=True,blank=True)
    usuario_creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_tramite = models.CharField(max_length=100, null=True, blank=True)
    estatus_doc = models.CharField(max_length=50, null=True, blank=True)
    notas_reporte = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Reportes Generados"

# --- SIGNALS ---
@receiver(post_save, sender=Documento)
def registrar_cambio_documento(sender, instance, created, **kwargs):
    accion = "NUEVO" if created else "MODIFICADO"
    ReporteGenerado.objects.create(
        cliente=instance.cliente,
        usuario_creador=instance.creado_por,
        tipo_tramite=instance.tipo.nombre_tipo,
        estatus_doc=instance.estado.nombre,
        notas_reporte=f"Registro {accion.lower()} exitosamente."
    )

@receiver(post_delete, sender=Documento)
def registrar_borrado_documento(sender, instance, **kwargs):
    ReporteGenerado.objects.create(
        cliente=instance.cliente,
        tipo_tramite=instance.tipo.nombre_tipo,
        estatus_doc="ELIMINADO",
        notas_reporte="Se eliminó el documento del sistema."
    )