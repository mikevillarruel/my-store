from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
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
    products = Product.objects.filter(deleted_at__isnull=True)[0:20]
    offers = Product.objects.filter(deleted_at__isnull=True, discount__isnull=False).order_by('-discount')[:10]
    latest = Product.objects.filter(deleted_at__isnull=True).order_by('-created_at')[:10]

    return render(request, 'products/home.html', {
        'products': products,
        'offers': offers,
        'latest': latest,
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


def search(request):
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    brands = request.GET.getlist('brands')
    sizes = request.GET.getlist('sizes')
    with_discount = request.GET.get('with_discount')
    in_stock = request.GET.get('in_stock')
    out_of_stock = request.GET.get('out_of_stock')

    if query:
        products = Product.objects.annotate(search=SearchVector('name', 'description', 'brand')).filter(search=query)
        brands_db = products.values_list('brand', flat=True).distinct()
        sizes_db = products.values_list('size', flat=True).distinct()

        if min_price:
            ids = [product.id for product in products if product.net_price >= int(min_price)]
            products = products.filter(id__in=ids)
        if max_price:
            ids = [product.id for product in products if product.net_price <= int(max_price)]
            products = products.filter(id__in=ids)
        if brands:
            products = products.filter(brand__in=brands)
        if sizes:
            products = products.filter(size__in=sizes)
        if with_discount:
            products = products.filter(discount__isnull=False)
        if not out_of_stock:
            products = products.filter(stock__gt=0)

        brands_to_send = get_filters(brands_db, brands)
        sizes_to_send = get_filters(sizes_db, sizes)

        return render(request, 'products/search.html', {
            'products': products,
            'query': query,
            'min_price': min_price,
            'max_price': max_price,
            'brands': brands_to_send,
            'sizes': sizes_to_send,
            'with_discount': with_discount,
            'in_stock': in_stock,
            'out_of_stock': out_of_stock,
        })
    else:
        return render(request, 'products/search.html')


def get_filters(filters, checked_filters):
    result = []
    for filter in filters:
        result.append({
            'name': filter,
            'checked': True if filter in checked_filters else False,
        })
    return result
