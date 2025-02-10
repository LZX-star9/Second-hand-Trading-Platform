from django import forms
from .models import Product

class NewListingForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ["title", "description", "price", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter product title"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Enter description"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        """重写 save 方法，确保 seller 被正确赋值"""
        product = super().save(commit=False)  # 先不保存到数据库
        if hasattr(self, 'seller'):
            product.seller = self.seller  # 赋值 seller
        if commit:
            product.save()
        return product