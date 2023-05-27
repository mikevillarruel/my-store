from django import forms

from .models import User


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control"

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        })
    )
