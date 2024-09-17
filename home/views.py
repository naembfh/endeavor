from django.shortcuts import render

# Example view function
def index(request):
    return render(request, 'base.html')