from django.contrib import admin
from mailing.models import Mailing, Log, Client


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_mail', 'end_mail', 'mail_time', 'status_mail', 'user')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('date_of_mail', 'status_of_mail', 'mailing',)
