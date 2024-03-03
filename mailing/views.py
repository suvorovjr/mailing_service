from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from mailing.models import Mailing, Client, Log
from django.core.cache import cache
from django.conf import settings
from blog.models import Blog
from mailing.forms import MailingForm, ClientForm
from django.urls import reverse_lazy


class IsAdminOrUserMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        return self.request.user == object.user or self.request.user.is_superuser


class IndexView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if settings.CACHE_ENABLED:
            blog_key = 'blog_list'
            count_key = 'counters'
            blog_list = cache.get(blog_key)
            counters = cache.get(count_key)
            if blog_list is None:
                blog_list = Blog.objects.order_by('-created_date')[:3]
                cache.set(blog_key, blog_list)
            if counters is None:
                mailing_count = Mailing.objects.count()
                mailing_active_count = Mailing.objects.filter(status_mail='started').count()
                clients_count = Client.objects.values('email').distinct().count()
                counters = {'mailing_count': mailing_count, 'mailing_active_count': mailing_active_count,
                            'clients_count': clients_count}
                cache.set(count_key, counters)
        else:
            blog_list = Blog.objects.order_by('-created_date')[:3]
            mailing_count = Mailing.objects.count()
            mailing_active_count = Mailing.objects.filter(status_mail='started').count()
            clients_count = Client.objects.values('email').distinct().count()
            counters = {'mailing_count': mailing_count, 'mailing_active_count': mailing_active_count,
                        'clients_count': clients_count}
        context_data['blog_list'] = blog_list
        context_data['counters'] = counters
        context_data['title'] = 'Главная'
        return context_data


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание рассылки'
        return context_data

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['clients'].queryset = self.request.user.client_set.all()
        return form

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.user = self.request.user
            self.object.user.save()
        return super().form_valid(form)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        context_data['object_list'] = Mailing.objects.filter(user=user)
        context_data['title'] = 'Мои рассылки'
        return context_data


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingUpdateView(LoginRequiredMixin, IsAdminOrUserMixin, UpdateView):
    model = Mailing
    success_url = reverse_lazy('mailing:list')
    form_class = MailingForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Редактирование рассылки | {self.object.mail_topic}'
        return context_data


class MailingDeleteView(LoginRequiredMixin, IsAdminOrUserMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Удаление рассылки | {self.object.mail_topic}'
        return context_data


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:list_client')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание клиента'
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.user = self.request.user
            self.object.save()
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        context_data['object_list'] = Client.objects.filter(user=user)
        context_data['title'] = 'Мои клиенты'
        return context_data


class ClientUpdateView(LoginRequiredMixin, IsAdminOrUserMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:list_client')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Редактирование клиента | {self.object.email}'
        return context_data


class ClientDeleteView(LoginRequiredMixin, IsAdminOrUserMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:list_client')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Удаление клиента | {self.object.email}'
        return context_data


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        context_data['object_list'] = Log.objects.filter(user=user)
        context_data['title'] = 'Логи'
        return context_data


class LogDeleteView(DeleteView):
    model = Log

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Удаление лога | {self.object.mailing}'
        return context_data
