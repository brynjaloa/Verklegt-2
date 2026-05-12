
from django import forms
from .models import Bid


class FormattedDecimalField(forms.DecimalField):
    def to_python(self, value):
        if isinstance(value, str):
            value = value.replace(",", "")

        return super().to_python(value)


class BidForm(forms.ModelForm):
    bid_price = FormattedDecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={
            'placeholder': 'Write bid here...',
            'class': 'bid-input bid-price-input',
            'inputmode': 'decimal',
            'autocomplete': 'off',
        }),
    )

    def __init__(self, *args, artwork=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.artwork = artwork

    class Meta:

        model = Bid

        fields = [
            'bid_price',
            'expiration_date'
        ]

        widgets = {

            'expiration_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'bid-input'
            }),
        }

    def clean_bid_price(self):
        bid_price = self.cleaned_data["bid_price"]

        if self.artwork and bid_price < self.artwork.starting_bid:
            raise forms.ValidationError(
                "Bid may not be lower than minimum bid, please bid again using a higher bid"
            )

        return bid_price
