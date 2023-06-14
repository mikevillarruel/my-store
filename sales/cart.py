import json

from django.http import HttpRequest


class CartItem:
    def __init__(self, product_id: int, quantity: int):
        self.product_id = product_id
        self.quantity = quantity


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

    def add(self, product_id: int, quantity: int):
        for item in self.items:
            if item.product_id == product_id:
                item.quantity += quantity
                self._add_values_to_session()
                return
        item = CartItem(product_id, quantity)
        self.items.append(item)
        self._add_values_to_session()

    def _add_values_to_session(self):
        self.session[self.ITEMS_SESSION_KEY] = json.dumps(self.items, default=lambda o: o.__dict__)
        self.session[self.COUNT_SESSION_KEY] = self.get_count()

    def get_count(self):
        count = 0
        for item in self.items:
            print(item)
            count += item.quantity
        return count

    def get_items(self):
        return self.items

    def get_quantity_by_product_id(self, product_id: int):
        if self.items:
            for item in self.items:
                if item.product_id == product_id:
                    return item.quantity
        return 0

    def clear(self):
        del self.session[self.ITEMS_SESSION_KEY]
        del self.session[self.COUNT_SESSION_KEY]
