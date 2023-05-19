from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control"

    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_at', 'modified_at', 'deleted_at', 'images']

    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        "multiple": True
    }))
