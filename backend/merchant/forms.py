from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Merchant, Restaurant,  Deliveryman

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


class MerchantForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )


from django import forms
from .models import Deliveryman

class DeliverymanForm(forms.ModelForm):
    Firstname = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Firstname', 'id': 'first-name'})
    )
    Lastname = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Lastname', 'id': 'last-name'})
    )
    Address = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Current address', 'id': 'address'})
    )
    Vehicle = forms.ChoiceField(
        required=True,
        choices=getattr(Deliveryman, 'VEHICLE_CHOICES', []),
        widget=forms.Select(attrs={'id': 'vehicletype'})
    )
    Zone = forms.ChoiceField(
        required=True,
        choices=getattr(Deliveryman, 'ZONE_CHOICES', []),
        widget=forms.Select(attrs={'id': 'deliveryzone'})
    )
    DutyTime = forms.ChoiceField(
        required=True,
        choices=getattr(Deliveryman, 'DUTYTIME_CHOICES', []),
        widget=forms.Select(attrs={'id': 'duty-time'})
    )
    VehicleNumber = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'BA 01 PA 1234 / 03-01-Pa-1234', 'id': 'vehicle-number'})
    )
    UserImage = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'id': 'identityimage', 'accept': 'image/*'})
    )
    PanNumber = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '9 digit pan number (123456789)', 'id': 'pan-number'})
    )
    DateofBirth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'id': 'dob'})
    )
    BillBookScanCopy = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'id': 'billBook', 'accept': 'image/*,application/pdf'})
    )

    class Meta:
        model = Deliveryman
        fields = [
            "Firstname",
            "Lastname",
            "Address",
            "Vehicle",
            "Zone",
            "DutyTime",
            "VehicleNumber",
            "UserImage",
            "PanNumber",
            "DateofBirth",
            "BillBookScanCopy",
        ]
        exclude = ['user', 'created_at', 'approved']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fname in ['Zone', 'Vehicle', 'DutyTime']:
            if fname in self.fields:
                self.fields[fname].choices = [(v, l) for v, l in self.fields[fname].choices if v != '']
                self.fields[fname].widget.attrs.setdefault('class', 'form-select')
        for name, field in self.fields.items():
            if field.required:
                field.widget.attrs.setdefault('required', 'required')


class RestaurantRegistrationForm(forms.ModelForm):
    restaurant_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: ABC Company',
            'id': 'restaurantname',
            'name': 'restaurantname'
        })
    )
    vat_and_tax = forms.DecimalField(
        required=True,
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'id': 'vatandtax',
            'name': 'vatandtax'
        })
    )
    restaurant_address = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'restaurantaddress',
            'name': 'restaurantaddress'
        })
    )
    latitude = forms.FloatField(
        required=True,
        widget=forms.TextInput(attrs={
            # 'readonly': True,
            'id': 'lat',
            'name': 'latitude'
        })
    )
    longitude = forms.FloatField(
        # required=True,
        widget=forms.TextInput(attrs={
            # 'readonly': True,
            'id': 'lng',
            'name': 'longitude'
        })
    )
    cuisine = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'list': 'cuisine-options',
            'placeholder': 'Select or type a cuisine',
            'id': 'cuisine',
            'name': 'cuisine'
        })
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'id': 'profile-pic',
            'name': 'profile-pic',
            'accept': 'image/*'
        })
    )
    cover_photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'id': 'cover-photo',
            'name': 'cover-photo',
            'accept': 'image/*'
        })
    )
    owner_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'owner-name',
            'name': 'owner-name',
        })
    )
    owner_contact = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'id': 'owner-contact',
            'name': 'owner-contact'
        })
    )
    menu = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'id': 'menu',
            'name': 'menu',
            'accept': '.png, .jpg, .jpeg, .pdf'
        })
    )

    class Meta:
        model = Restaurant
        fields = [
            'restaurant_name', 'vat_and_tax', 'restaurant_address',
            'latitude', 'longitude', 'cuisine',
            'profile_picture', 'cover_photo',
            'owner_name', 'owner_contact',
            'menu',
        ]
        exclude = ['user']


class BusinessPlanForm(forms.ModelForm):
    business_plan = forms.ChoiceField(
        required=True,
        choices=Restaurant.BUSINESS_PLAN_CHOICES
    )

    class Meta:
        model = Restaurant
        fields = ['business_plan']
