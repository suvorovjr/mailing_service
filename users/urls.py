from users.apps import UsersConfig
from users.views import LoginView, UserCreateView, ProfileView, CustomPasswordResetView, activate_user, \
    CustomPasswordResetConfirmView, CustomPasswordResetDoneView, CustomPasswordResetCompleteView, ProfileUpdateView
from django.contrib.auth.views import LogoutView
from django.urls import path

app_name = UsersConfig.name

urlpatterns = [
    path('auth/', UserCreateView.as_view(), name='auth'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('confirm/<str:token>', activate_user, name='confirm'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
