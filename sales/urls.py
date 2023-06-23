from django.urls import path

from . import views

urlpatterns = [
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('delete_item_from_cart/<int:product_id>', views.delete_item_from_cart, name='delete_item_from_cart'),
    path('update_item_quantity/', views.update_item_quantity, name='update_item_quantity'),
]
