import random

from django.core.mail import send_mail


def generate_confirmation_code():
    return (''.join([
        random.choice(list(
            '123456789qwertyuiopasdQWERTYUIOPASD'
        )) for x in range(10)
    ]))


def send_mail_to_user(email, confirmation_code):
    send_mail(
        message='Спасибо за регистрацию.'
                f'Код подтверждения: {confirmation_code}',
        from_email='project@gmail.com',
        recipient_list=[email],
        fail_silently=False,
    )
