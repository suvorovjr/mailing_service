from django import forms
from mailing.models import Mailing
from users.forms import StylesMixin


class MailingForm(StylesMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('user',)
