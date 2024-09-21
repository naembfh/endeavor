from django.shortcuts import render, redirect
from django.http import JsonResponse
from home.models import Plant, Order
import json
from decimal import Decimal
from django.views.decorators.http import require_POST
import stripe
from django.conf import settings

# Set your Stripe secret API key
stripe.api_key = settings.STRIPE_SECRET_KEY


@require_POST
def create_checkout_session(request):
    cart_cookie = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart_cookie)

    # Initialize subtotal and tax rate
    subtotal = Decimal('0.00')
    tax_rate = Decimal('0.07')  # 7% tax rate

    # Prepare line items for Stripe checkout
    line_items = []
    
    for plant_id, quantity in cart.items():
        try:
            plant = Plant.objects.get(id=plant_id)  # Get the plant details
            price = plant.price  # Get the price from the plant object
            
            # Calculate subtotal
            subtotal += price * quantity
            
            # Calculate the price per item including tax
            price_with_tax = price + (price * tax_rate)
            
            # Add plant details to Stripe line items with tax included
            line_items.append({
                'price_data': {
                    'currency': 'myr',
                    'product_data': {
                        'name': plant.common_name,  # Use the plant's common name
                    },
                    'unit_amount': int(price_with_tax * 100),  # Stripe requires the amount in cents
                },
                'quantity': quantity,
            })
        except Plant.DoesNotExist:
            return JsonResponse({'error': f'Plant with id {plant_id} not found.'}, status=400)

    # Create Stripe checkout session with line items
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/success_view/'),
        cancel_url=request.build_absolute_uri('/cancel_view/'),
    )
    
    return JsonResponse({'id': session.id})


def success_view(request):
    # Get cart from cookies
    cart_cookie = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart_cookie)
    print(cart)

    subtotal = Decimal('0.00')
    tax_rate = Decimal('0.07')  # 7% tax rate
    total_amount = Decimal('0.00')

    if request.user.is_authenticated:
        for plant_id, quantity in cart.items():
            try:
                plant = Plant.objects.get(id=plant_id)
                subtotal += plant.price * quantity
            except Plant.DoesNotExist:
                continue  # Skip if the plant doesn't exist

        # Calculate tax amount and total amount
        tax_amount = subtotal * tax_rate
        total_amount = subtotal + tax_amount

        # Save order to the database with payment method as 'card'
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            cart_data=json.dumps(cart),  # Save the cart data
            pay_method='card'  # Payment method
        )
        
        print(order)
        # Clear the cart cookie after order is created
        response = redirect('order_confirmation')  # Redirect to an order confirmation page
        response.delete_cookie('cart')
        return response
    else:
        return redirect('login')  # Redirect to login if not authenticated


def order_confirmation_view(request):
    return render(request, 'include/stripe/orderConfirm.html')


def cancel_view(request):
    # Redirect to a cancel page or back to cart
    return render(request, 'include/stripe/cancel.html')

def pay_by_cash_view(request):
    cart_cookie = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart_cookie)

    subtotal = Decimal('0.00')
    tax_rate = Decimal('0.07')  # 7% tax rate
    total_amount = Decimal('0.00')

    if request.user.is_authenticated:
        for plant_id, quantity in cart.items():
            try:
                plant = Plant.objects.get(id=plant_id)
                subtotal += plant.price * quantity
            except Plant.DoesNotExist:
                continue 

        # Calculate tax amount and total amount
        tax_amount = subtotal * tax_rate
        total_amount = subtotal + tax_amount

        # Save order to the database with payment method as 'cash'
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            cart_data=json.dumps(cart), 
            pay_method='cash' 
        )
        
        # Clear the cart cookie after order is created
        response = redirect('order_confirmation') 
        response.delete_cookie('cart')
        return response
    else:
        return redirect('login')

def my_orders_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    current_orders = Order.objects.filter(user=request.user, isDelivery=False)
    past_orders = Order.objects.filter(user=request.user, isDelivery=True)

    current_orders_details = []
    for order in current_orders:
        cart = order.get_cart()
        products = []
        for plant_id, quantity in cart.items():
            try:
                plant = Plant.objects.get(id=plant_id)
                products.append({
                    'name': plant.common_name,
                    'price': float(plant.price),
                    'quantity': quantity,
                    'total_price': float(plant.price * quantity),
                    'image_url': plant.image.url
                })
            except Plant.DoesNotExist:
                continue
        current_orders_details.append({'order': order, 'products': products})

    past_orders_details = []
    for order in past_orders:
        cart = order.get_cart()
        products = []
        for plant_id, quantity in cart.items():
            try:
                plant = Plant.objects.get(id=plant_id)
                products.append({
                    'name': plant.common_name,
                    'price': float(plant.price),
                    'quantity': quantity,
                    'total_price': float((plant.price * quantity)),
                    'image_url': plant.image.url  
                })
            except Plant.DoesNotExist:
                continue
        past_orders_details.append({'order': order, 'products': products})

    context = {
        'current_orders_details': current_orders_details,
        'past_orders_details': past_orders_details,
    }
    return render(request, 'include/myOrders.html', context)

