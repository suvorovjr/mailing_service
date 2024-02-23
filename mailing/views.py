from django.views.generic import TemplateView
from blog.models import Blog


class IndexView(TemplateView):
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        blog_news = Blog.objects.order_by('-created_date')[:3]
        context_data['blog_list'] = blog_news
        return context_data
