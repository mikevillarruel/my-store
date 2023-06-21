from django.contrib import messages
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

            messages.success(request, f'{product.name} has been created successfully.')

            return redirect('my_products')
        else:
            context = {'form': form}
    else:
        context = {'form': ProductCreationForm()}

    return render(request, 'products/create_product.html', context)


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
    messages.success(request, f'{product.name} has been deleted successfully.')
    return redirect('my_products')


def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'products/product_detail.html', {
        'product': product,
    })


@login_required
def edit_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            context = {
                'form': ProductForm(instance=product),
                'images_creation_form': ImagesCreationForm(),
            }
            messages.success(request, f'{product.name} has been updated successfully.')
        else:
            context = {'form': form}
    else:
        context = {
            'form': ProductForm(instance=product),
            'images_creation_form': ImagesCreationForm(),
        }

    return render(request, 'products/edit_product.html', context)


@login_required
def delete_images(request):
    if request.method == 'POST':
        images = request.POST.getlist('images')

        if not images:
            return redirect(request.META.get('HTTP_REFERER'))  # Redirect to the previous page

        product = Image.objects.get(id=images[0]).product

        for image_id in images:
            image = Image.objects.get(id=image_id)
            image.delete()

        messages.success(request, f'{product.name} has been updated successfully.')

        return redirect('edit_product', id=product.id)


@login_required
def add_images_to_product(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = ImagesCreationForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('add_images')

            for image in images:
                product.images.create(path=image)

            messages.success(request, f'{product.name} has been updated successfully.')

            return redirect('edit_product', id=product_id)
        else:
            return render(request, 'products/edit_product.html', {
                'form': ProductForm(instance=product),
                'images_creation_form': form,
            })
