# users/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Seller

class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'profile_image']


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = [
            'seller_type',
            'street_name',
            'city',
            'postal_code',
            'logo',
            'cover_image',
            'bio',
        ]