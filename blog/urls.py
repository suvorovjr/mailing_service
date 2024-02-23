from blog.apps import BlogConfig
from django.urls import path
from blog.views import BlogListView, BlogCreateView, BlogDeleteView, BlogDetailView, BlogUpdateView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='list'),
    path('create', BlogCreateView.as_view(), name='create'),
    path('update/<slug:slug>/', BlogUpdateView.as_view(), name='update'),
    path('detail/<slug:slug>/', BlogDetailView.as_view(), name='detail'),
    path('delete/<slug:slug>/', BlogDeleteView.as_view(), name='delete'),
]
