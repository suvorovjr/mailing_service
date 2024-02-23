from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from blog.forms import BlogForm
from django.urls import reverse_lazy
from blog.models import Blog
from pytils.translit import slugify
from django.core.paginator import Paginator


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

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
        return context_data


class BlogDetailView(DetailView):
    model = Blog


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm

    def get_success_url(self):
        slug = self.object.slug
        return reverse_lazy('blog:detail', kwargs={'slug': slug})

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')
