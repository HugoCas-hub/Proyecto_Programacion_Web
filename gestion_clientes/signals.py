from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from .models import Documento

@receiver(post_save, sender=Documento)
def enviar_correo_documento(sender, instance, created, **kwargs):

    if created:
        send_mail(
            subject='Nuevo documento registrado',
            message=f'Se creó el documento: {instance}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.cliente.email],
            fail_silently=False,
        )

        print("Correo enviado correctamente")