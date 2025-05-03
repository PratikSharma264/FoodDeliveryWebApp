from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Merchant, Restaurant, Deliveryman

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
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )


class DeliverymanForm(forms.ModelForm):
    Firstname = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Firstname'})
    )
    Lastname = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Lastname'})
    )
    Email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'abc@gmail.com'})
    )
    DeliveryType = forms.ChoiceField(
        required=True,
        choices=Deliveryman.DELIVERY_TYPE_CHOICES,
        widget=forms.Select()
    )
    Zone = forms.ChoiceField(
        required=True,
        choices=Deliveryman.ZONE_CHOICES,
        widget=forms.Select()
    )
    Vehicle = forms.ChoiceField(
        required=True,
        choices=Deliveryman.VEHICLE_CHOICES,
        widget=forms.Select()
    )
    IdentityType = forms.ChoiceField(
        required=True,
        choices=Deliveryman.IDENTITY_CHOICES,
        widget=forms.Select()
    )
    IdentityNumber = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'ID number'})
    )
    IdentityImage = forms.ImageField(required=True)
    PanNumber = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': '9 digit pan number (123456789)', 'pattern': r'\d{9}'})
    )
    BillBookScanCopy = forms.ImageField(required=True)
    DutyTime = forms.ChoiceField(
        required=True,
        choices=Deliveryman.DUTYTIME_CHOICES,
        widget=forms.Select()
    )
    VehicleNumber = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder': 'BA 01 PA 1234 / 03-01-Pa-1234'})
    )
    DateofBirth = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'})
    )
    UserImage = forms.ImageField(required=True)

    class Meta:
        model = Deliveryman
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fname in ['DeliveryType', 'Zone', 'Vehicle', 'IdentityType', 'DutyTime']:
            self.fields[fname].choices = [
                (v, l) for v, l in self.fields[fname].choices if v != '']
