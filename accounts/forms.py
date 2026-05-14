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

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('This username is already in use.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already in use.')

        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'profile_image']


class SellerForm(forms.ModelForm):
    address_help_text = "This address is only shown publicly for gallery sellers."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'name': 'Seller or gallery name',
            'street_name': 'Street address',
            'city': 'City',
            'postal_code': 'Postal code',
            'bio': 'Tell buyers about you or your gallery',
        }

        for field_name, field in self.fields.items():
            field.required = True
            field.widget.attrs.setdefault('class', 'seller-field')

            if field_name in placeholders:
                field.widget.attrs.setdefault('placeholder', placeholders[field_name])

        self.fields['bio'].widget.attrs.setdefault('rows', 5)
        self.fields['street_name'].help_text = self.address_help_text

    class Meta:
        model = Seller
        fields = [
            'name',
            'seller_type',
            'street_name',
            'city',
            'postal_code',
            'logo',
            'cover_image',
            'bio',
        ]


class SellerEditForm(forms.ModelForm):
    address_help_text = "This address is only shown publicly for gallery sellers."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'name': 'Seller or gallery name',
            'street_name': 'Street address',
            'city': 'City',
            'postal_code': 'Postal code',
            'bio': 'Tell buyers about you or your gallery',
        }

        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'seller-field')

            if field_name in placeholders:
                field.widget.attrs.setdefault('placeholder', placeholders[field_name])

        self.fields['name'].required = True
        self.fields['street_name'].required = True
        self.fields['city'].required = True
        self.fields['postal_code'].required = True
        self.fields['bio'].required = True
        self.fields['bio'].widget.attrs.setdefault('rows', 5)
        self.fields['street_name'].help_text = self.address_help_text

    class Meta:
        model = Seller
        fields = [
            'name',
            'street_name',
            'city',
            'postal_code',
            'logo',
            'cover_image',
            'bio',
        ]
