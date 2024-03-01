from django.contrib import admin
from mailing.models import Mailing, Log, Client


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_mail', 'end_mail', 'mail_time', 'status_mail', 'user')
