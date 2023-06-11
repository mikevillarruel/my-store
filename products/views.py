from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import ProductForm, ProductCreationForm, ImagesCreationForm
from .models import Product, Image


# Create your views here.
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductCreationForm(request.POST, request.FILES)
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
            'form': ProductCreationForm()
        })


def home(request):
    products = Product.objects.filter(deleted_at__isnull=True)
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


@login_required
def edit_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            images = request.FILES.getlist('images')

            for image in images:
                product.images.create(path=image)

        else:
            return render(request, 'products/edit_product.html', {
                'form': form,
            })

    return render(request, 'products/edit_product.html', {
        'form': ProductForm(instance=product),
        'images_creation_form': ImagesCreationForm(),
    })


@login_required
def delete_images(request):
    if request.method == 'POST':
        images = request.POST.getlist('images')

        if not images:
            return redirect(request.META.get('HTTP_REFERER'))  # Redirect to the previous page

        product_id = Image.objects.get(id=images[0]).product.id

        for image_id in images:
            image = Image.objects.get(id=image_id)
            image.delete()

        return redirect('edit_product', id=product_id)


@login_required
def add_images_to_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ImagesCreationForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('add_images')

            for image in images:
                product.images.create(path=image)

            return redirect('edit_product', id=product_id)
        else:
            return render(request, 'products/edit_product.html', {
                'form': ProductForm(instance=product),
                'images_creation_form': form,
            })
