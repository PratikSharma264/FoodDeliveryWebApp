from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Merchant(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='merchant_profile')
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(
        regex=r'^(?:((98|97|96)\d{8})|(0\d{2,3}\d{6}))$',
        message="Enter a valid Nepali mobile or landline number"
    )])
