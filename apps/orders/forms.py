from django import forms

from apps.orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.TextInput())
    address = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
