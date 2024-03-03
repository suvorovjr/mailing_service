from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from blog.forms import BlogForm
from django.urls import reverse_lazy
from blog.models import Blog
from pytils.translit import slugify
from django.core.paginator import Paginator


class BlogCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'blog.add_blog'
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Создание статьи'
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        object_list = context_data['object_list']
        paginator = Paginator(object_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except Exception as e:
            object_list = paginator.page(1)
        context_data['object_list'] = object_list
        context_data['title'] = 'Статьи'
        return context_data


class BlogDetailView(DetailView):
    model = Blog

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Статья | {self.object.title[:25]}'
        return context_data

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'blog.change_blog'
    model = Blog
    form_class = BlogForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Редактирование статьи | {self.object.title[:25]}'
        return context_data

    def get_success_url(self):
        slug = self.object.slug
        return reverse_lazy('blog:detail', kwargs={'slug': slug})

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'blog.delete_blog'
    model = Blog
    success_url = reverse_lazy('blog:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = f'Удаление статьи | {self.object.title[:25]}'
        return context_data
