from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Plant, Review
import decimal
import json
from django.http import HttpRequest
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.contrib import messages

def index(request:HttpRequest):
    context = {
        'plants': Plant.objects.all(),
        'reviews': Review.objects.all(),
        'current_path': request.path, 
    }
    return render(request, 'include/home/home.html', context)

def about(request):
    return render(request, 'include/about.html')

def cart_view(request):
    # Get all plants
    plants = Plant.objects.all()

    # Get cart from cookies
    cart_cookie = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart_cookie)

    # Prepare context with cart items
    cart_items = []
    for plant_id, quantity in cart.items():
        try:
            plant = plants.get(id=plant_id)
            cart_items.append({
                'id': plant.id,
                'name': plant.common_name,
                'price': plant.price,
                'quantity': quantity,
                'image_url': plant.image.url
            })
        except Plant.DoesNotExist:
            # Handle case where plant is not found
            continue

    # Calculate totals
    total_items = sum(cart.values())
    
    # Convert prices and quantities to Decimal for accurate calculations
    subtotal = sum(decimal.Decimal(item['price']) * decimal.Decimal(item['quantity']) for item in cart_items)
    tax_rate = decimal.Decimal('0.07')  # Tax rate as Decimal
    tax_amount = subtotal * tax_rate
    total_amount = subtotal + tax_amount

    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total_amount': total_amount
    }

    return render(request, 'include/cart/cart.html', context)


def shop_view(request: HttpRequest):
    plant_list = Plant.objects.all()
    paginator = Paginator(plant_list, 4)  # Show 10 plants per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'plants': page_obj,
        'page_obj': page_obj,
        'current_path': request.path,
    }
    return render(request, 'include/plants.html', context)

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        print(form)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user 
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('home')  
        else:
            messages.error(request, 'There was an error with your submission. Please try again.')
    else:
        form = ReviewForm()

    return render(request, 'include/home/home.html',)