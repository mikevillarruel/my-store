from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ProductForm
from .models import Product


# Create your views here.
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data.pop('images')
            product = Product.objects.create(**form.cleaned_data, user=request.user)
            images = request.FILES.getlist('images')

            for image in images:
                product.images.create(path=image)

            return redirect('create_product')
        else:
            return render(request, 'products/create_product.html', {
                'form': form,
            })
    else:
        return render(request, 'products/create_product.html', {
            'form': ProductForm()
        })
