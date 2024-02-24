from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import IndexView, ClientCreateView, ClientListView, ClientUpdateView, ClientDeleteView
from mailing.views import MailingCreateView, MailingListView, MailingDetailView, MailingUpdateView, MailingDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create_mailing/', MailingCreateView.as_view(), name='create'),
    path('list_mailing/', MailingListView.as_view(), name='list'),
    path('detail_mailing/<int:pk>/', MailingDetailView.as_view(), name='detail'),
    path('update_mailing/<int:pk>/', MailingUpdateView.as_view(), name='update'),
    path('delete_mailing/<int:pk>/', MailingDeleteView.as_view(), name='delete'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('list_client/', ClientListView.as_view(), name='list_client'),
    path('update_client/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),
]
