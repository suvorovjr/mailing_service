from django.core.mail import send_mail
from django.conf import settings


def send_verification_password(email, verification_link):
    send_mail(
        subject='Подтвердите аккаунт',
        message=f'Чтобы подтвердить аккаунт перейдите по ссылке: {verification_link}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
