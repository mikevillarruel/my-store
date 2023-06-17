import json

from django.http import HttpRequest

from products.models import Product


class CartItem:
    def __init__(self, product_id: int, quantity: int):
        self.product_id = product_id
        self.quantity = quantity

    def get_product(self) -> Product:
        return Product.objects.get(id=self.product_id)


class Cart:
    ITEMS_SESSION_KEY = 'cart_items'
    COUNT_SESSION_KEY = 'items_count'

    def __init__(self, request: HttpRequest):
        self.request = request
        self.session = request.session
        self.items = []
        cart = self.session.get(self.ITEMS_SESSION_KEY)

        if cart:
            cart = json.loads(cart)
            print(cart)
            for item in cart:
                id_product = int(item['product_id'])
                quantity = int(item['quantity'])
                self.add(id_product, quantity)

    def add(self, product_id: int, quantity: int) -> bool:
        product = Product.objects.get(id=product_id)
        if product.stock < self.get_quantity_by_product_id(product_id) + quantity:
            return False

        for item in self.items:
            if item.product_id == product_id:
                item.quantity += quantity
                self._add_values_to_session()
                return True

        item = CartItem(product_id, quantity)
        self.items.append(item)
        self._add_values_to_session()
        return True

    def _add_values_to_session(self):
        self.session[self.ITEMS_SESSION_KEY] = json.dumps(self.items, default=lambda o: o.__dict__)
        self.session[self.COUNT_SESSION_KEY] = self.get_count()

    def get_count(self) -> int:
        count = 0
        for item in self.items:
            print(item)
            count += item.quantity
        return count

    def get_items(self) -> list[CartItem]:
        return self.items

    def get_quantity_by_product_id(self, product_id: int) -> int:
        if self.items:
            for item in self.items:
                if item.product_id == product_id:
                    return item.quantity
        return 0

    def clear(self):
        del self.session[self.ITEMS_SESSION_KEY]
        del self.session[self.COUNT_SESSION_KEY]

    def delete_item_by_product_id(self, product_id: int) -> bool:
        result = False
        for item in self.items:
            if item.product_id == product_id:
                self.items.remove(item)
                self._add_values_to_session()
                result = True
                break

        if not self.items:
            self.clear()

        return result
