from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create_product, name='create_product'),
    path('my_products/', views.my_products, name='my_products'),
    path('delete/<int:id>/', views.delete_product, name='delete_product'),
]
