from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart-count/', views.cart_count, name='cart_count'),
    path('cart/', views.cart_view, name='cart'),
]