from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.crypto import get_random_string
from django.shortcuts import redirect
from users.services import send_verification_password
from django.views.generic import CreateView, DetailView
from django.urls import reverse_lazy
from users.models import User
from users.forms import UserForm, LoginForm, CustomPasswordResetForm, CustomSetPasswordForm, ProfileUpdateForm
from django.urls import reverse


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    form_class = LoginForm


class UserCreateView(CreateView):
    template_name = 'users/signup.html'
    form_class = UserForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.verification_token = get_random_string(30)
        verification_link = f'http://{get_current_site(self.request)}/users/confirm/{user.verification_token}'
        send_verification_password(user.email, verification_link)
        user.save()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user


def activate_user(request, token):
    user = User.objects.get(verification_token=token)
    user.verification_token = ''
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    template_name = 'users/password_reset.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/update_profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
