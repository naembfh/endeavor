from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Profile, Review

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
@receiver(post_save, sender=Review)
def update_plant_rating(sender, instance, **kwargs):
    instance.plant.update_rating()

@receiver(post_delete, sender=Review)
def update_plant_rating_on_delete(sender, instance, **kwargs):
    instance.plant.update_rating()

