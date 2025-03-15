from django import forms

from apps.listings.models import Product
from apps.users.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'address', 'balance', 'is_staff', 'is_superuser']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'seller', 'is_sold']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'seller': forms.Select(attrs={'class': 'form-control'}),
            'is_sold': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }