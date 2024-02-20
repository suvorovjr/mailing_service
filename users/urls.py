from users.apps import UsersConfig
from users.views import LoginView, UserCreateView, activate_user
from django.urls import path

app_name = UsersConfig.name

urlpatterns = [
    path('auth/', UserCreateView.as_view(), name='auth'),
    path('login/', LoginView.as_view(), name='login'),
    path('confirm/<str:token>', activate_user, name='confirm')
]
