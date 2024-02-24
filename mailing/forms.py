from django import forms
from mailing.models import Mailing, Client
from users.forms import StylesMixin


class MailingForm(StylesMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('user',)


class ClientForm(StylesMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('user',)
