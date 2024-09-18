from django.db import models

class Plant(models.Model):
    scientific_name = models.CharField(max_length=255)
    common_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='plants/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    
    def __str__(self):
        return self.common_name