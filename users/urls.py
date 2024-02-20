from users.apps import UsersConfig
from django.urls import path
from users.views import index

app_name = UsersConfig.name

urlpatterns = [
    path('', index, name='registration'),
]
