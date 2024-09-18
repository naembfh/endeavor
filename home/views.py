from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Plant

# Example view function
def index(request):
    plants = Plant.objects.all()
    context = {
        "plants" : plants,
    }
    return render(request, 'include/home/home.html', context)

def about(request):
    return render(request, 'include/about.html')


def cart_view(request):
    # Fake data for the cart
    cart_items = [
        {
            'id': '1',
            'name': 'Fitness Band',
            'price': 59.99,
            'quantity': 2,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'id': '2',
            'name': 'Yoga Mat',
            'price': 29.99,
            'quantity': 1,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'id': '3',
            'name': 'Yoga Mat',
            'price': 29.99,
            'quantity': 1,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'id': '4',
            'name': 'Yoga Mat',
            'price': 29.99,
            'quantity': 1,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'id': '5',
            'name': 'Yoga Mat',
            'price': 29.99,
            'quantity': 1,
            'image_url': 'https://via.placeholder.com/150'
        },
        {
            'id': '6',
            'name': 'Yoga Mat',
            'price': 29.99,
            'quantity': 1,
            'image_url': 'https://via.placeholder.com/150'
        },
    ]
    
    # Fake order summary
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    tax_amount = subtotal * 0.1  # Assuming 10% tax
    total_amount = subtotal + tax_amount
    total_items = sum(item['quantity'] for item in cart_items)

    # Pass the fake data to the template
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'total_items': total_items,
    }

    return render(request, 'include/cart/cart.html', context)