from django import forms
from .models import Review, Profile

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [ 'comment', 'rating', 'plant']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['img', 'first_name', 'last_name', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-gray-100 text-yellow-500',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-gray-100 text-yellow-500',
                'placeholder': 'Enter your last name'
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-gray-100 text-yellow-500',
                'placeholder': 'Enter your address'
            }),
            'img': forms.ClearableFileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:border-transparent bg-gray-100 text-yellow-500',
            }),
        }

