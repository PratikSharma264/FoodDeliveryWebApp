from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Merchant, Restaurant


class MerchantSignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email address", widget=forms.EmailInput(
        attrs={'class': 'form-control', 'id': 'email', 'required': True}))
    first_name = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'firstName', 'required': True}))
    last_name = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'lastName', 'required': True}))
    company_name = forms.CharField(label="Company Name", max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'companyName', 'required': True}))
    phone_number = forms.CharField(label="Phone Number", max_length=15, validators=[RegexValidator(
        regex=r'^(?:((98|97|96)\d{8})|(0\d{2,3}\d{6}))$',
        message="Enter a valid Nepali mobile or landline number"
    )], widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'phoneNumber', 'required': True}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(MerchantSignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'id': 'username',
            'required': True,
        })
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
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            # Now save Merchant model instance
            Merchant.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                phone_number=self.cleaned_data['phone_number']
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
