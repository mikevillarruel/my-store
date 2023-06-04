from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserForm, LoginForm, UserUpdateForm
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
            return redirect('home')
        else:
            return render(request, 'authentication/login.html', {
                'form': LoginForm(),
                'error_message': 'Invalid username or password.',
            })
    else:
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'authentication/login.html', {
            'form': LoginForm(),
        })


@login_required
def account(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
        else:
            return render(request, 'authentication/account.html', {
                'form': form
            })
    else:
        return render(request, 'authentication/account.html', {
            'form': UserUpdateForm(instance=request.user),
        })


def logout(request):
    _logout(request)
    return redirect('login')
