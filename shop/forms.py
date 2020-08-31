from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm as RegistrationForm

from shop.models import UserProfile

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("address", "phone", "postal_code", "city")


class SigninForm(AuthenticationForm):

    class Meta:
        fields = ("username", "password")


class SignupForm(RegistrationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta(RegistrationForm.Meta):
        fields = ("username", "email", "first_name", "last_name")
