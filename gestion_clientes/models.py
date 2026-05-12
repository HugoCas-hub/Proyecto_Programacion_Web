from django.db import models
from django.contrib.auth.models import AbstractUser

# =========================
# 1. TABLA USUARIOS
# =========================
class Usuario(AbstractUser):
    # Heredamos de AbstractUser para que sigas pudiendo entrar al /admin
    # Pero mapeamos los campos a la estructura de Hugo
    nombre = models.CharField(max_length=100, db_column='nombre')
    rol_choices = [('admin', 'admin'), ('empleado', 'empleado')]
    rol = models.CharField(max_length=20, choices=rol_choices, default='empleado', db_column='rol')
    creado_en = models.DateTimeField(auto_now_add=True, db_column='creado_en')

    class Meta:
        db_table = 'usuarios'

# =========================
# 2. TABLA CLIENTES
# =========================
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True, db_column='id_cliente')
    nombre = models.CharField(max_length=150, db_column='nombre')
    telefono = models.CharField(max_length=20, null=True, blank=True, db_column='telefono')
    email = models.EmailField(max_length=100, null=True, blank=True, db_column='email')
    direccion = models.CharField(max_length=150, null=True, blank=True, db_column='direccion')
    creado_en = models.DateTimeField(auto_now_add=True, db_column='creado_en')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'clientes'

# =========================
# 3. TABLA TIPOS DE DOCUMENTOS
# =========================
class TipoDocumento(models.Model):
    id_tipo = models.AutoField(primary_key=True, db_column='id_tipo')
    nombre_tipo = models.CharField(max_length=100, db_column='nombre_tipo')
    dias_alerta = models.IntegerField(default=30, db_column='dias_alerta')

    def __str__(self):
        return self.nombre_tipo

    class Meta:
        db_table = 'tipos_documentos'

# =========================
# 4. TABLA ESTADOS (REEMPLAZA ENUM)
# =========================
class EstadoDocumento(models.Model):
    id_estado = models.AutoField(primary_key=True, db_column='id_estado')
    nombre = models.CharField(max_length=50, db_column='nombre')
    color = models.CharField(max_length=20, db_column='color')

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'estados_documento'

# =========================
# 5. TABLA DOCUMENTOS (MEJORADA)
# =========================
class Documento(models.Model):
    id_documento = models.AutoField(primary_key=True, db_column='id_documento')
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, db_column='id_cliente')
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, db_column='id_tipo')
    estado = models.ForeignKey(EstadoDocumento, on_delete=models.SET_NULL, null=True, db_column='id_estado')

    fecha_vencimiento = models.DateField(null=True, blank=True, db_column='fecha_vencimiento')
    notas = models.TextField(null=True, blank=True, db_column='notas')
    fecha_detencion = models.DateField(null=True, blank=True, db_column='fecha_detencion')

    # Django maneja archivos por ruta, Hugo pidió LONGBLOB. 
    # Usamos FileField para que funcione el upload, pero apuntando a su nombre de columna.
    archivo = models.FileField(upload_to='documentos/', null=True, blank=True, db_column='archivo')
    nombre_archivo = models.CharField(max_length=255, null=True, blank=True, db_column='nombre_archivo')
    tipo_mime = models.CharField(max_length=100, null=True, blank=True, db_column='tipo_mime')
    tamano = models.IntegerField(null=True, blank=True, db_column='tamano')

    creado_por = models.ForeignKey(Usuario, related_name='docs_creados', on_delete=models.SET_NULL, null=True, db_column='creado_por')
    modificado_por = models.ForeignKey(Usuario, related_name='docs_modificados', on_delete=models.SET_NULL, null=True, db_column='modificado_por')
    creado_en = models.DateTimeField(auto_now_add=True, db_column='creado_en')

    class Meta:
        db_table = 'documentos'

# =========================
# 6. TABLA NOTIFICACIONES
# =========================
class Notificacion(models.Model):
    id_notificacion = models.AutoField(primary_key=True, db_column='id_notificacion')
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, db_column='id_documento')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='id_usuario')
    mensaje = models.TextField(db_column='mensaje')
    tipo_choices = [('alerta', 'alerta'), ('vencido', 'vencido')]
    tipo = models.CharField(max_length=20, choices=tipo_choices, db_column='tipo')
    fecha_creacion = models.DateTimeField(auto_now_add=True, db_column='fecha_creacion')
    enviado = models.BooleanField(default=False, db_column='enviado')

    class Meta:
        db_table = 'notificaciones'

# =========================
# 7. TABLA HISTORIAL (AUDITORÍA)
# =========================
class HistorialDocumento(models.Model):
    id_historial = models.AutoField(primary_key=True, db_column='id_historial')
    documento = models.ForeignKey(Documento, on_delete=models.CASCADE, db_column='id_documento')
    estado_anterior = models.CharField(max_length=50, db_column='estado_anterior')
    estado_nuevo = models.CharField(max_length=50, db_column='estado_nuevo')
    fecha_cambio = models.DateTimeField(auto_now_add=True, db_column='fecha_cambio')
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, db_column='id_usuario')
    comentario = models.TextField(null=True, blank=True, db_column='comentario')

    class Meta:
        db_table = 'historial_documentos'

# =========================
# 8. CONFIGURACIÓN DE ALERTAS
# =========================
class ConfiguracionAlerta(models.Model):
    id_config = models.AutoField(primary_key=True, db_column='id_config')
    dias_rojo = models.IntegerField(db_column='dias_rojo')
    dias_amarillo = models.IntegerField(db_column='dias_amarillo')
    activo = models.BooleanField(default=True, db_column='activo')
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE, db_column='id_tipo')

    class Meta:
        db_table = 'configuracion_alertas'

# =========================
# 9. TABLA REPORTES
# =========================
class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True, db_column='id_reporte')
    tipo_reporte = models.CharField(max_length=100, db_column='tipo_reporte')
    fecha_generacion = models.DateTimeField(auto_now_add=True, db_column='fecha_generacion')
    generado_por = models.ForeignKey(Usuario, on_delete=models.CASCADE, db_column='generado_por')
    parametros = models.JSONField(db_column='parametros')

    class Meta:
        db_table = 'reportes'

# =========================
# 10. TABLA LOGS (EVENTOS DEL SISTEMA)
# =========================
class Log(models.Model):
    id_log = models.AutoField(primary_key=True, db_column='id_log')
    accion = models.CharField(max_length=100, db_column='accion')
    tabla_afectada = models.CharField(max_length=50, db_column='tabla_afectada')
    id_registro = models.IntegerField(db_column='id_registro')
    fecha = models.DateTimeField(auto_now_add=True, db_column='fecha')
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, db_column='id_usuario')

    class Meta:
        db_table = 'logs'

class ReporteGenerado(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='reportes_personalizados/')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte de {self.cliente.nombre} - {self.creado_en.strftime('%Y-%m-%d')}"

class NotaReporte(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota para {self.cliente.nombre} - {self.fecha_creacion}"