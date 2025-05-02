from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Merchant, Restaurant

phone_validator = RegexValidator(
    regex=r'^(?:((98|97|96)\d{8})|(0\d{2,3}\d{6}))$',
    message="Enter a valid Nepali mobile or landline number"
)


class MerchantSignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'required': True
        })
    )
    name = forms.CharField(
        label="Full Name",
        max_length=250,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'name',
            'required': True
        })
    )
    phone_number = forms.CharField(
        label="Phone Number",
        max_length=15,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'phoneNumber',
            'required': True
        })
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(MerchantSignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'id': 'password',
            'required': True,
            'minlength': '8'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'id': 'confirmPassword',
            'required': True
        })

    def save(self, commit=True):
        user = super(MerchantSignUpForm, self).save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Merchant.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                phone_number=self.cleaned_data['phone_number'],
            )
        return user


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'restaurant_name',
            'restaurant_contact_name',
            'contact_number',
            'secondary_contact_number',
            'city',
            'restaurant_address',
            'cuisine',
            'latitude',
            'longitude',
        ]
        widgets = {
            'restaurant_name': forms.TextInput(attrs={'class': 'form-control'}),
            'restaurant_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'secondary_contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'restaurant_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cuisine': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class MerchantForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
