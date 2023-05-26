from django.shortcuts import render, redirect

from .forms import UserForm


# Create your views here.
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_user')
        else:
            return render(request, 'authentication/create_user.html', {
                'form': form,
            })
    else:
        return render(request, 'authentication/create_user.html', {
            'form': UserForm()
        })
