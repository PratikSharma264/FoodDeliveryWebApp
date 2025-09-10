from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.conf import settings
from .models import Merchant, Restaurant, Deliveryman, FoodItem
phone_validator = RegexValidator(
    regex=r'^(?:((98|97|96)\d{8})|(0\d{2,3}\d{6}))$',
    message="Enter a valid Nepali mobile or landline number"
)

vehicle_validator = RegexValidator(
    regex=r'^(?:[A-Z]{1,2}[-\s]?\d{1,2}[-\s]?[A-Z]{1,2}[-\s]?\d{1,4}|\d{1,2}-\d{1,2}-[A-Z]{1,3}-\d{1,4})$',
    message="Enter a valid vehicle number (e.g. 'BA 01 PA 1234', 'BA-07-PA-1234', or '3-01-PA-1234')."
)


class MerchantSignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'id': 'email', 'required': True})
    )
    name = forms.CharField(
        label="Full Name",
        max_length=250,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'name', 'required': True})
    )
    phone_number = forms.CharField(
        label="Phone Number",
        max_length=15,
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'phoneNumber', 'required': True})
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'id': 'password', 'required': True, 'minlength': '8'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'id': 'confirmPassword', 'required': True})

    def save(self, commit=True):
        user = super().save(commit=False)
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

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registered. Please use another.")
        return email


class MerchantForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )


class DeliverymanForm(forms.ModelForm):
    Firstname = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Firstname', 'id': 'first-name'}))
    Lastname = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Lastname', 'id': 'last-name'}))
    Address = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Current address', 'id': 'address'}))
    Vehicle = forms.ChoiceField(required=True, choices=getattr(
        Deliveryman, 'VEHICLE_CHOICES', []), widget=forms.Select(attrs={'id': 'vehicletype'}))
    Zone = forms.ChoiceField(required=True, choices=getattr(
        Deliveryman, 'ZONE_CHOICES', []), widget=forms.Select(attrs={'id': 'deliveryzone'}))
    DutyTime = forms.ChoiceField(required=True, choices=getattr(
        Deliveryman, 'DUTYTIME_CHOICES', []), widget=forms.Select(attrs={'id': 'duty-time'}))
    VehicleNumber = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'BA 01 PA 1234 / 03-01-Pa-1234', 'id': 'vehicle-number'}))
    UserImage = forms.ImageField(required=True, widget=forms.ClearableFileInput(
        attrs={'id': 'identityimage', 'accept': 'image/*'}))
    PanNumber = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': '9 digit PAN number (123456789)', 'id': 'pan-number'}))
    DateofBirth = forms.DateField(required=True, widget=forms.DateInput(
        attrs={'type': 'date', 'id': 'dob'}))
    BillBookScanCopy = forms.FileField(required=True, widget=forms.ClearableFileInput(
        attrs={'id': 'billBook', 'accept': 'image/*,application/pdf'}))

    class Meta:
        model = Deliveryman
        fields = ["Firstname", "Lastname", "Address", "Vehicle", "Zone", "DutyTime",
                  "VehicleNumber", "UserImage", "PanNumber", "DateofBirth", "BillBookScanCopy"]
        exclude = ['user', 'created_at', 'approved']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fname in ['Zone', 'Vehicle', 'DutyTime']:
            if fname in self.fields:
                self.fields[fname].choices = [
                    (v, l) for v, l in self.fields[fname].choices if v != '']
                self.fields[fname].widget.attrs.setdefault(
                    'class', 'form-select')
        for name, field in self.fields.items():
            if field.required:
                field.widget.attrs.setdefault('required', 'required')


class RestaurantRegistrationForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['restaurant_name', 'restaurant_address', 'latitude', 'longitude',
                  'cuisine', 'description', 'profile_picture', 'cover_photo',
                  'owner_name', 'owner_contact', 'owner_email', 'menu', 'restaurant_type']
        exclude = ['user', 'created_at', 'approved']


class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = [
            'name',
            'price',
            'discount',
            'veg_nonveg',
            'availability_status',
            'profile_picture',
            'description',
        ]


class RestaurantBioUpdateForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['restaurant_name', 'restaurant_address',
                  'description', 'owner_name', 'owner_contact', 'owner_email',  'restaurant_type']
        exclude = ['user', 'created_at', 'latitude', 'longitude',
                   'profile_picture', 'cover_photo', 'menu', 'cuisine', 'approved']


class RestaurantProfilePicUpdateForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['profile_picture']
        exclude = ['user', 'created_at', 'latitude', 'longitude',
                   'cover_photo', 'menu', 'cuisine', 'approved', 'restaurant_name', 'restaurant_address',
                   'description', 'owner_name', 'owner_contact', 'owner_email',  'restaurant_type']


# class BusinessPlanForm(forms.ModelForm):
#     class Meta:
#         model = Restaurant
