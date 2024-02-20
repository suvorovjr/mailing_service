from django.contrib.auth.views import LoginView as BaseLoginView
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy
from users.models import User
from users.forms import UserForm, LoginForm


class LoginView(BaseLoginView):
    model = User
    template_name = 'users/login.html'
    form_class = LoginForm


class UserCreateView(CreateView):
    model = User
    template_name = 'users/signup.html'
    form_class = UserForm
    success_url = reverse_lazy('users:auth')
