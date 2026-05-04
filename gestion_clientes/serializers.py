from rest_framework import serializers
from .models import Cliente, Documento, TipoDocumento, HistorialDocumento, EstadoDocumento

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoDocumento
        fields = '__all__'

class DocumentoSerializer(serializers.ModelSerializer):
    # Traemos los nombres reales en lugar de solo los IDs numéricos
    tipo_nombre = serializers.ReadOnlyField(source='tipo.nombre_tipo')
    estado_nombre = serializers.ReadOnlyField(source='estado.nombre_estado')
    color_estado = serializers.ReadOnlyField(source='estado.color')
    cliente_nombre = serializers.ReadOnlyField(source='cliente.nombre')

    class Meta:
        model = Documento
        fields = [
            'id', 'cliente_nombre', 'tipo_nombre', 'fecha_vencimiento', 
            'estado_nombre', 'color_estado', 'archivo', 'notas'
        ]

class ClienteListSerializer(serializers.ModelSerializer):
    # Esto permite que al consultar un cliente veas todos sus documentos asociados
    documentos = DocumentoSerializer(many=True, read_only=True)

    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'documentos']

class HistorialSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username')
    
    class Meta:
        model = HistorialDocumento
        fields = ['id', 'estado_anterior', 'estado_nuevo', 'fecha_cambio', 'usuario_nombre', 'comentario']