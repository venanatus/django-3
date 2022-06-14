from django import forms
from django.contrib.auth.models import User
from .bulma_mixin import BulmaMixin
from .models import Review, RATE_CHOICES


class OrderForm(BulmaMixin, forms.ModelForm):
    address = forms.CharField(label='Address')
    phone = forms.CharField(label='Phone')

    class Meta:
        model = User
        fields = ['address', 'phone']


class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}), label='Write review text')
    rate = forms.ChoiceField(choices=RATE_CHOICES, required=True, label='Rate product from 1 to 5')

    class Meta:
        model = Review
        fields = ['text', 'rate']
