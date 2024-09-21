from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart_view, name='cart'),
    path('add-review/', views.add_review, name='add_review'),
    path('login/', views.login_view, name='login'),
    path('forget-password/', views.forgot_password_view, name='forgot_password'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('create-profile/', views.create_or_update_profile, name='profile'),
    
]