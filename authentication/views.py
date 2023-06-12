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
            context = {'form': form}
    else:
        context = {'form': UserForm()}

    return render(request, 'authentication/sign_up.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            _login(request, user)
            return redirect('home')
        else:
            context = {
                'form': LoginForm(),
                'error_message': 'Invalid username or password.',
            }
    else:
        context = {'form': LoginForm()}

    return render(request, 'authentication/login.html', context)


@login_required
def account(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
        else:
            context = {'form': form}
    else:
        context = {'form': UserUpdateForm(instance=request.user)}

    return render(request, 'authentication/account.html', context)


def logout(request):
    _logout(request)
    return redirect('login')
