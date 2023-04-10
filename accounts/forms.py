from django import forms
from .models import Address


# Create your forms here.
class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ("name", "street", "city", "postcode")
