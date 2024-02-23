from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from blog.models import Blog


class BlogListView(ListView):
    model = Blog


class BlogCreateView(CreateView):
    pass


class BlogDetailView(DetailView):
    pass


class BlogUpdateView(UpdateView):
    pass


class BlogDeleteView(DeleteView):
    pass
