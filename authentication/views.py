from django.contrib.auth import authenticate, login as _login
from django.shortcuts import render, redirect

from .forms import UserForm, LoginForm
from .models import User


# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect('login')
        else:
            return render(request, 'authentication/sign_up.html', {
                'form': form,
            })
    else:
        return render(request, 'authentication/sign_up.html', {
            'form': UserForm()
        })


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            _login(request, user)
            return redirect('create_product')
        else:
            return render(request, 'authentication/login.html', {
                'form': LoginForm(),
                'error_message': 'Invalid username or password.',
            })
    else:
        return render(request, 'authentication/login.html', {
            'form': LoginForm(),
        })
