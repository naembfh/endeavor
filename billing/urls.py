from django.urls import path
from . import views

urlpatterns = [
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success_view/', views.success_view, name='success_view'),
    path('cancel_view/', views.cancel_view, name='cancel_view'),
    path('order_confirmation/', views.order_confirmation_view, name='order_confirmation'),
    path('pay-by-cash/', views.pay_by_cash_view, name='pay_by_cash'),
     path('my-orders/', views.my_orders_view, name='my_orders'),
]
