from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    # URL to handle adding books to the cart
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    # URL route to view the shopping cart page
    path('cart/', views.view_cart, name='view_cart'),
    
]