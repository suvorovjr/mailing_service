from typing import Tuple
from django.core.mail import send_mail
from django.db.models import Q
from mailing.models import Client, Mailing, Log
from users.models import User
from django.utils import timezone
from django.conf import settings
from datetime import timedelta, datetime
from pytz import timezone as tz


def send_email_to_client(subject: str, message: str, client_email: str) -> Tuple[str, str]:
    """
    Отправляет электронное письмо клиенту.
    :param subject: Тема сообщения.
    :param message: Текст сообщения.
    :param client_email: Адрес электронной почты клиента.
    :return: Кортеж, содержащий статус отправки и ответ сервера.
    """

    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [client_email],
            fail_silently=False
        )
        return 'sent', 'Email sent successfully'
    except Exception as e:
        return 'error', str(e)


def log_email_status(mailing: Mailing, status: str, server_response: str, user: User) -> None:
    """
    Логирует статус отправленного электронного письма.
    :param mailing: Объект рассылки.
    :param status: Статус отправки ('sent', 'error').
    :param server_response: Ответ сервера или описание ошибки.
    :param user: Объект пользователя.
    """

    Log.objects.create(
        date_of_mail=timezone.now(),
        status_of_mail=status,
        answer=server_response,
        mailing=mailing,
        user=user
    )


def send_emails() -> None:
    """
    Отправляет электронные письма согласно установленному расписанию и статусу рассылки.

    Проходит через все рассылки и проверяет, пора ли отправить следующее письмо.
    Отправляет письма всем клиентам, подписанным на рассылку.
    """
    current_time = timezone.now().time()

    now = timezone.now()
    mailings = Mailing.objects.filter(
        Q(start_date__lte=now) | Q(start_date__isnull=True),
        Q(end_date__gte=now) | Q(end_date__isnull=True)
    ).filter(Q(status='created') | (Q(status='started') & Q(send_time__lte=current_time)))
    for mailing in mailings:

        if is_time_to_send(mailing):
            user = mailing.user
            clients = mailing.clients
            message_subject = mailing.mail_topic
            message_body = mailing.mail_message
            for client in clients:
                status, server_response = send_email_to_client(message_subject, message_body, client.email)
                log_email_status(mailing, status, server_response, user)
                if mailing.status == 'created':
                    mailing.status = 'started'
                    mailing.save()


def is_time_to_send(mailing: Mailing) -> bool:
    """
    Определяет, пора ли отправить следующее письмо в рассылке.

    :param mailing: Объект рассылки.
    :return: True, если пора отправить письмо, иначе False.
    """

    moscow_tz = tz('Europe/Moscow')
    send_time = moscow_tz.localize(datetime.combine(datetime.now().date(), mailing.mail_time))

    # Обработка для рассылок со статусом "created"
    if mailing.status_mail == 'created':
        return send_time <= moscow_tz.localize(datetime.now())

    # Обработка для рассылок со статусом "started"
    elif mailing.status_mail == 'started':
        try:
            last_log_entry = Log.objects.filter(mailing=mailing).latest('sent_datetime')
            if mailing.frequency_mail == 'daily':
                period = timedelta(days=1)
            elif mailing.frequency_mail == 'weekly':
                period = timedelta(weeks=1)
            elif mailing.frequency_mail == 'monthly':
                period = timedelta(days=30)

            return last_log_entry.sent_datetime + period <= moscow_tz.localize(
                datetime.now()) and send_time <= moscow_tz.localize(datetime.now())
        except Log.DoesNotExist:
            return False
