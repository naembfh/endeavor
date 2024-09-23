from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpRequest
from .models import Plant, Review, Profile
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings
import json

from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.contrib.auth import logout, get_user_model, login
import json
import decimal
from .models import Plant
from django.conf import settings
from django.shortcuts import render, redirect

def index(request: HttpRequest):
    # Get the top 4 plants with the highest ratings
    top_plants = Plant.objects.order_by('-rating')[:4]
    
    # Get the top 5 most recent reviews
    recent_reviews = Review.objects.order_by('-created_at')[:5]
    
    context = {
        'plants': top_plants,
        'reviews': recent_reviews,
        'current_path': request.path,
    }
    
    return render(request, 'include/home/home.html', context)

def about(request):
    return render(request, 'include/about.html')

def shop_view(request: HttpRequest):
    plant_list = Plant.objects.all()
    paginator = Paginator(plant_list, 4)  

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

    return render(request, 'include/home/home.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url_path = request.POST.get('next')
        next_url = next_url_path.strip('/')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}! You have successfully logged in.')

            print("Redirecting to:", next_url)  
            return redirect(next_url if next_url else 'home')   
        else:
            messages.error(request, 'The email or password you entered is incorrect. Please try again.')

    return render(request, 'include/auth/login.html')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='password_reset_email.html',
            )
            messages.success(request, 'We have sent you an email to reset your password. Please check your inbox.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid email address. Please enter a valid email associated with your account.')

    return render(request, 'include/auth/forgot_password.html')

def register_view(request):
    User = get_user_model()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if email or username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose a different one.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already associated with an account. Please use another email.')
        else:
            # Create and authenticate the new user
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created successfully, and you are now logged in.')
            return redirect('home')

    return render(request, 'include/auth/register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

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
    tax_rate = decimal.Decimal('0.07')  
    tax_amount = subtotal * tax_rate
    total_amount = subtotal + tax_amount
  
    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, 'include/cart/cart.html', context)

@login_required
def create_or_update_profile(request):
    try:
        # Check if the user already has a profile
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profileCreate.html', {'form': form})