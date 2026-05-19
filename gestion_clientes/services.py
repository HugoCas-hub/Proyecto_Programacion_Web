from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from .models import Documento


def revisar_documentos_proximos():

    hoy = timezone.now().date()
    limite = hoy + timedelta(days=7)

    # DOCUMENTOS VENCIDOS O PRÓXIMOS A VENCER
    documentos = Documento.objects.filter(
        fecha_vencimiento__lte=limite
    )

    enviados = 0

    for documento in documentos:

        cliente = documento.cliente

        # SI NO TIENE CORREO, CONTINUAR
        if not cliente.email:
            continue

        # =========================
        # DOCUMENTO VENCIDO
        # =========================
        if documento.fecha_vencimiento < hoy:

            asunto = 'Documento vencido'

            mensaje = (
                f'Hola {cliente.nombre},\n\n'
                f'Tu documento "{documento.tipo.nombre_tipo}" '
                f'venció el {documento.fecha_vencimiento}.\n\n'
                f'Favor de renovarlo lo antes posible.'
            )

        # =========================
        # DOCUMENTO PRÓXIMO A VENCER
        # =========================
        else:

            asunto = 'Documento próximo a vencer'

            mensaje = (
                f'Hola {cliente.nombre},\n\n'
                f'Tu documento "{documento.tipo.nombre_tipo}" '
                f'vence el {documento.fecha_vencimiento}.\n\n'
                f'Favor de renovarlo antes de la fecha límite.'
            )

        # ENVIAR CORREO
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[cliente.email],
            fail_silently=False,
        )

        enviados += 1

    return enviados