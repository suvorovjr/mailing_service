from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import IndexView, MailingCreateView, ClientCreateView, ClientListView, ClientUpdateView, \
    ClientDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create_mailing/', MailingCreateView.as_view(), name='create'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('list_client/', ClientListView.as_view(), name='list_client'),
    path('update_client/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
]
