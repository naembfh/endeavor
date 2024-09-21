from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Plant,Review,Profile,Order


admin.site.register(Plant)
admin.site.register(User, UserAdmin)
admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(Order)
