from users.apps import UsersConfig
from users.views import LoginView, UserCreateView, ProfileView, activate_user
from django.contrib.auth.views import LogoutView
from django.urls import path

app_name = UsersConfig.name

urlpatterns = [
    path('auth/', UserCreateView.as_view(), name='auth'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('confirm/<str:token>', activate_user, name='confirm')
]
