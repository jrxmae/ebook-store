from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    # URL to handle adding books to the cart
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    # URL route to view the shopping cart page
    path('cart/', views.view_cart, name='view_cart'),
    # URL to handle removing books from the cart
    path('remove-from-cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:book_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:book_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    
]