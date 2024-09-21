from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import Avg
import json

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    img = models.ImageField(upload_to='user_images/', null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.email} Profile'

    def get_profile_image(self):
        if self.img and hasattr(self.img, 'url'):
            return self.img.url
        return "https://upload.wikimedia.org/wikipedia/commons/7/72/Default-welcomer.png?20180610185859"

class Plant(models.Model):
    scientific_name = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='plants/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

    def __str__(self):
        return self.common_name

    def update_rating(self):
        reviews = self.review_set.all()
        if reviews.exists():
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            self.rating = round(average_rating or 0.0, 1)
        else:
            self.rating = 0.0
        self.save()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=0)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.plant.common_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.plant.update_rating()

class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('cash', 'Cash'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    cart_data = models.TextField()
    pay_method = models.CharField(max_length=50, default='cash') 

    def __str__(self):
        return f'Order {self.id} by {self.user.email}'

  
    def get_cart(self):
        return json.loads(self.cart_data) 
