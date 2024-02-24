from django import forms
from django.forms import SelectDateWidget
from mailing.models import Mailing, Client
from users.forms import StylesMixin


class MailingForm(StylesMixin, forms.ModelForm):
    start_mail = forms.DateField(
        widget=SelectDateWidget(attrs={'class': 'date-input'}),
    )
    end_mail = forms.DateField(
        widget=SelectDateWidget(attrs={'class': 'date-input'}),
    )

    class Meta:
        model = Mailing
        exclude = ('user',)


class ClientForm(StylesMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('user',)
