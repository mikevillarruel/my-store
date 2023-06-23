from django.contrib import messages
from django.shortcuts import redirect, render

from products.models import Product
from .cart import Cart, StockException


# Create your views here.
def add_to_cart(request):
    if request.method == 'POST':
        cart = Cart(request)
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))
        product = Product.objects.get(id=product_id)

        try:
            cart.add(product_id, quantity)
            messages.success(
                request,
                message=f"{quantity} {'item' if quantity == 1 else 'items'} of {product.name} added to the cart."
            )
        except StockException as e:
            messages.error(request, message=e.message)

        return redirect('product_detail', id=product_id)


def cart_detail(request):
    cart = Cart(request)
    items = [
        {
            'product': item.get_product(),
            'quantity': item.quantity,
            'subtotal': item.get_product().net_price * item.quantity,
        }
        for item in cart.get_items()
    ]

    subtotal = sum([item['subtotal'] for item in items])

    return render(request, 'sales/cart_detail.html', {
        'items': items,
        'subtotal': subtotal,
    })


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')


def delete_item_from_cart(request, product_id):
    cart = Cart(request)
    cart.delete_item_by_product_id(product_id)
    return redirect('cart_detail')


def update_item_quantity(request):
    if request.method == 'POST':
        cart = Cart(request)
        quantity = int(request.POST.get('quantity'))
        product_id = int(request.POST.get('product_id'))
        try:
            cart.update_item_quantity(product_id, quantity)
            messages.success(request, message='Quantity updated successfully.')
        except StockException as e:
            messages.error(request, message=e.message)

        return redirect('cart_detail')
