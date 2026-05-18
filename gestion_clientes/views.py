from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Cliente, Documento, TipoDocumento, 
    EstadoDocumento, ReporteGenerado, Usuario
)
from .serializers import (
    ClienteListSerializer, DocumentoSerializer, 
    TipoDocumentoSerializer, EstadoSerializer, 
    ReporteGeneradoSerializer
)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('nombre')
    serializer_class = ClienteListSerializer
    permission_classes = [permissions.AllowAny]

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        
        documento = serializer.save(creado_por=user)

        send_mail(
            subject='Nuevo documento registrado',
            message=f'Se registró el documento: {documento.nombre}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['destino@gmail.com'],
            fail_silently=False,
        )

    def perform_update(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(creado_por=user)

class ReporteGeneradoViewSet(viewsets.ModelViewSet):
    # Ordenamos por fecha para que lo más nuevo salga primero en React
    queryset = ReporteGenerado.objects.all().order_by('-fecha_creacion')
    serializer_class = ReporteGeneradoSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(usuario_creador=user)

class TipoDocumentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer
    permission_classes = [permissions.AllowAny]

class EstadoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EstadoDocumento.objects.all()
    serializer_class = EstadoSerializer
    permission_classes = [permissions.AllowAny]