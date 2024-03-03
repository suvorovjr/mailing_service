from datetime import datetime
from django.db import models
from users.models import User, NULLABLE


class Client(models.Model):
    email = models.EmailField(verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    comment = models.TextField(verbose_name='Комментарий')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', **NULLABLE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    FREQUENCY_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )
    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    )
    start_mail = models.DateField(verbose_name='Дата начала рассылки')
    end_mail = models.DateField(verbose_name='Дата окончания рассылки')
    mail_time = models.TimeField(verbose_name='Время рассылки')
    status_mail = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус рассылки')
    frequency_mail = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, verbose_name='Периодичность рассылки')
    clients = models.ManyToManyField(Client, verbose_name='Клиенты', related_name='mailings')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, **NULLABLE)
    mail_topic = models.CharField(max_length=255, verbose_name='Тема письма')
    mail_message = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Log(models.Model):
    date_of_mail = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')
    status_of_mail = models.BooleanField(verbose_name='Статус попытки')
    answer = models.TextField(verbose_name='Ответ сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, **NULLABLE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.date_of_mail}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
