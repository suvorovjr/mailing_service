from django import forms
from blog.models import Blog
from users.forms import StylesMixin


class BlogForm(StylesMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'imagine')
