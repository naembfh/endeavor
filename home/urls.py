from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart_view, name='cart'),
    path('add-review/', views.add_review, name='add_review'),
]