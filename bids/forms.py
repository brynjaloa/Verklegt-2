
from django import forms
from .models import Bid


class BidForm(forms.ModelForm):

    class Meta:

        model = Bid

        fields = [
            'bid_price',
            'expiration_date'
        ]

        widgets = {

            'bid_price': forms.NumberInput(attrs={
                'placeholder': 'Write bid here...',
                'class': 'bid-input'
            }),

            'expiration_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'bid-input'
            }),
        }