from users.apps import UsersConfig
from users.views import LoginView, UserCreateView
from django.urls import path

app_name = UsersConfig.name

urlpatterns = [
    path('auth/', UserCreateView.as_view(), name='auth'),
    path('login/', LoginView.as_view(), name='login'),
]
