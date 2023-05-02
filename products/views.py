from django.shortcuts import render, redirect

from .forms import ProductForm
from .models import Product, Image


# Create your views here.
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            Product.objects.create(
                **{key: value for key, value in form.cleaned_data.items() if key != 'path'}
            )

            images = request.FILES.getlist('path')

            for image in images:
                Image.objects.create(path=image)

            return redirect('create_product')
        else:
            return render(request, 'create_product.html', {
                'form': form,
            })
    else:
        return render(request, 'create_product.html', {
            'form': ProductForm()
        })
