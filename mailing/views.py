from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from mailing.models import Mailing, Client, Log
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
        blog_news = Blog.objects.order_by('-created_date')[:3]
        context_data['blog_list'] = blog_news
        return context_data


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:list')

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
        return context_data


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing


class MailingUpdateView(LoginRequiredMixin, IsAdminOrUserMixin, UpdateView):
    model = Mailing
    success_url = reverse_lazy('mailing:list')
    form_class = MailingForm


class MailingDeleteView(LoginRequiredMixin, IsAdminOrUserMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:list')


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:list_client')

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
        return context_data


class ClientUpdateView(LoginRequiredMixin, IsAdminOrUserMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:list_client')


class ClientDeleteView(LoginRequiredMixin, IsAdminOrUserMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:list_client')


class LogCreateView(CreateView):
    pass


class LogListView(LoginRequiredMixin, ListView):
    model = Log
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        context_data['object_list'] = Log.objects.filter(user=user)
        return context_data


class LogDetailView(DetailView):
    pass


class LogDeleteView(DeleteView):
    pass
