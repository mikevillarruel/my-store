from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_at', 'modified_at', 'deleted_at']

    path = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        "multiple": True
    }))
