from django.contrib import messages
from django.shortcuts import redirect

from products.models import Product
from .cart import Cart


# Create your views here.
def add_to_cart(request):
    if request.method == 'POST':
        cart = Cart(request)
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))
        product = Product.objects.get(id=product_id)
        total_quantity = cart.get_quantity_by_product_id(product_id) + quantity

        if total_quantity <= product.stock:
            cart.add(product_id, quantity)
        else:
            messages.error(
                request,
                message=f"You can't add more than {product.stock} items "
                        f"of this product to the cart because of the stock."
            )

        return redirect('product_detail', id=product_id)
