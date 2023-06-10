from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create_product, name='create_product'),
    path('my_products/', views.my_products, name='my_products'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),
    path('product_detail/<int:id>/', views.product_detail, name='product_detail'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    path('delete_image/<int:id>/', views.delete_image, name='delete_image'),
    path('add_images_to_product/<int:product_id>/', views.add_images_to_product, name='add_images_to_product'),
]
