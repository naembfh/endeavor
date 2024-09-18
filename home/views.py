from django.shortcuts import render
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