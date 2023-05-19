from django.shortcuts import render, redirect

from .forms import ProductForm


# Create your views here.
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
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
