from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from mailing.models import Mailing, Client
from blog.models import Blog
from mailing.forms import MailingForm, ClientForm
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        blog_news = Blog.objects.order_by('-created_date')[:3]
        context_data['blog_list'] = blog_news
        return context_data


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:list_client')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.user = self.request.user
            self.object.save()
        return super().form_valid(form)


class ClientListView(ListView):
    model = Client

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        context_data['object_list'] = Client.objects.filter(user=user)
        return context_data


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:list_client')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:list_client')
