from django import forms
from django.utils import timezone
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["expiration_date"].widget.attrs["min"] = timezone.localdate().isoformat()

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data["expiration_date"]

        if expiration_date < timezone.localdate():
            raise forms.ValidationError("Expiration date cannot be in the past.")

        return expiration_date


class ContactInformationForm(forms.Form):
    COUNTRY_CHOICES = [
        ("Iceland", "Iceland"),
        ("Denmark", "Denmark"),
        ("Norway", "Norway"),
        ("Sweden", "Sweden"),
        ("Finland", "Finland"),
        ("United Kingdom", "United Kingdom"),
        ("United States", "United States"),
        ("Germany", "Germany"),
        ("France", "France"),
        ("Spain", "Spain"),
    ]

    street_name = forms.CharField(max_length=255)
    city = forms.CharField(max_length=120)
    postal_code = forms.CharField(max_length=20)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES)
    national_id = forms.RegexField(
        regex=r"^\d+$",
        max_length=20,
        label="National id",
        error_messages={"invalid": "Use numbers only."},
        widget=forms.TextInput(attrs={
            "inputmode": "numeric",
            "placeholder": "1234567890",
        }),
    )


class PaymentInformationForm(forms.Form):
    PAYMENT_CHOICES = [
        ("credit_card", "Credit card"),
        ("bank_transfer", "Bank transfer"),
        ("wire_transfer", "Wire transfer"),
    ]

    payment_option = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect,
    )
    cardholder_name = forms.CharField(max_length=120, required=False)
    credit_card_number = forms.RegexField(
        regex=r"^\d{16}$",
        required=False,
        error_messages={"invalid": "Enter exactly 16 numbers."},
        widget=forms.TextInput(attrs={
            "inputmode": "numeric",
            "maxlength": "16",
            "placeholder": "1234123412341234",
        }),
    )
    expiry_month = forms.ChoiceField(
        choices=[("", "Month")] + [(f"{month:02d}", f"{month:02d}") for month in range(1, 13)],
        required=False,
    )
    expiry_year = forms.ChoiceField(
        choices=[("", "Year")] + [
            (str(year), str(year))
            for year in range(timezone.now().year, timezone.now().year + 16)
        ],
        required=False,
    )
    cvc = forms.RegexField(
        regex=r"^\d{3,4}$",
        required=False,
        label="CVV",
        error_messages={"invalid": "Enter 3 or 4 numbers."},
        widget=forms.TextInput(attrs={
            "inputmode": "numeric",
            "maxlength": "4",
            "placeholder": "123",
        }),
    )
    bank_account = forms.RegexField(
        regex=r"^\d+$",
        required=False,
        error_messages={"invalid": "Use numbers only."},
        widget=forms.TextInput(attrs={
            "inputmode": "numeric",
            "placeholder": "0000000000",
        }),
    )
    sending_bank_name = forms.CharField(max_length=120, required=False)
    routing_number = forms.RegexField(
        regex=r"^\d+$",
        required=False,
        error_messages={"invalid": "Use numbers only."},
        widget=forms.TextInput(attrs={
            "inputmode": "numeric",
            "placeholder": "123456789",
        }),
    )
    account_number = forms.RegexField(
        regex=r"^\d+$",
        required=False,
        error_messages={"invalid": "Use numbers only."},
        widget=forms.TextInput(attrs={
            "inputmode": "numeric",
            "placeholder": "1234567890",
        }),
    )

    def clean(self):
        cleaned_data = super().clean()
        payment_option = cleaned_data.get("payment_option")

        required_fields = {
            "credit_card": [
                "cardholder_name",
                "credit_card_number",
                "expiry_month",
                "expiry_year",
                "cvc",
            ],
            "bank_transfer": ["bank_account"],
            "wire_transfer": [
                "sending_bank_name",
                "routing_number",
                "account_number",
            ],
        }

        for field_name in required_fields.get(payment_option, []):
            if field_name not in self.errors and not cleaned_data.get(field_name):
                self.add_error(field_name, "This field is required.")

        return cleaned_data
