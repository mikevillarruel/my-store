from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

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

            return redirect('my_products')
        else:
            return render(request, 'products/create_product.html', {
                'form': form,
            })
    else:
        return render(request, 'products/create_product.html', {
            'form': ProductForm()
        })


def home(request):
    products = Product.objects.all()
    return render(request, 'products/home.html', {
        'products': products,
    })


@login_required
def my_products(request):
    products = Product.objects.filter(user=request.user, deleted_at__isnull=True)
    return render(request, 'products/my_products.html', {
        'products': products,
    })


@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.deleted_at = timezone.now()
    product.save()
    return redirect('my_products')


def product_detail(request, id):
    product = Product.objects.get(id=id)
    price_with_discount = product.price - (product.price * product.discount / 100) if product.discount else None
    return render(request, 'products/product_detail.html', {
        'product': product,
        'price_with_discount': price_with_discount,
    })
