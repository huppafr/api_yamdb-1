import uuid
from django.conf import settings
from django.core.mail import send_mail


def generate_confirmation_code():
    return uuid.uuid1()


def send_mail_to_user(email, confirmation_code):
    send_mail(
        'Спасибо за регистрацию.',
        f'Код подтверждения: {confirmation_code}',
        from_email=settings.EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
