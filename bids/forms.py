from django import forms
from .models import Bid
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

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
class ContactInformationForm(forms.Form):
    street_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'finalize-input'}))
    city = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'finalize-input'}))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'finalize-input'}))
    country = CountryField().formfield(widget=CountrySelectWidget(attrs={'class': 'finalize-input'}))
    national_id = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'finalize-input'}))


PAYMENT_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('bank_transfer', 'Bank Transfer'),
    ('wire_transfer', 'Wire Transfer'),
]


class PaymentInformationForm(forms.Form):
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)
    cardholder_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'finalize-input'}))
    credit_card_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'finalize-input'}))
    expiry_date = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'finalize-input', 'placeholder': 'MM/YY'}))
    cvc = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'finalize-input'}))
    bank_account = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'finalize-input'}))
    sending_bank_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'finalize-input'}))
    routing_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'finalize-input'}))
    account_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'finalize-input'}))