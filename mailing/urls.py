from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import index

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='index'),
]
