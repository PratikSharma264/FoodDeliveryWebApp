from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser, Group, Permission

# Validator for Nepali phone numbers
phone_validator = RegexValidator(
    regex=r'^(?:((98|97|96)\d{8})|(0\d{2,3}\d{6}))$',
    message="Enter a valid Nepali mobile or landline number"
)

vehicle_validator = RegexValidator(
    regex=(
        r'^(?:'
        r'[A-Z]{1,2}\s?\d{1,2}\s?[A-Z]{1,2}\s?\d{1,4}'
        r'|\d{1,2}-\d{1,2}-[A-Za-z]{1,3}-\d{1,4}'
        r')$'
    ),
    message="Enter a valid vehicle number"
)


class Merchant(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='merchant_profile')
    phone_number = models.CharField(
        max_length=15, validators=[phone_validator])
    name = models.CharField(max_length=250, null=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  

    def __str__(self):
        try:
            return f"{self.appuser_profile.name} ({self.email})"
        except:
            return f"{self.username} ({self.email})"

    def get_full_name(self):
        try:
            return self.appuser_profile.name
        except:
            return self.username

    def get_initials(self):
        try:
            name = self.appuser_profile.name
            name_parts = name.split()
            if len(name_parts) >= 2:
                return f"{name_parts[0][0].upper()}{name_parts[-1][0].upper()}"
            return name_parts[0][0].upper() if name_parts else "U"
        except:
            return self.username[0].upper() if self.username else "U"


class AppUser(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='appuser_profile', null=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15, validators=[phone_validator])
    address = models.TextField()
    
    def __str__(self):
        return f"{self.name} ({self.phone_number})"


class Cuisine(models.Model):
    cuisine_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cuisine_name


class Restaurant(models.Model):
    RESTAURANT_TYPE_CHOICES = [
        ('local', 'Local'),
        ('finedining', 'Fine Dining'),
    ]
    BUSINESS_PLAN_CHOICES = [
        ('commission', 'Commission Base'),
        ('subscription', 'Subscription Base'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurant_profile', null=True)
    restaurant_name = models.CharField(max_length=100, default='')
    vat_and_tax = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0)
    restaurant_address = models.TextField(default='')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    cuisine = models.CharField(max_length=50, default='')
    profile_picture = models.ImageField(
        upload_to='restaurant/profile_pics/', blank=True, null=True)
    cover_photo = models.ImageField(
        upload_to='restaurant/cover_photos/', blank=True, null=True)
    external_image_url = models.URLField(blank=True, null=True) 
    owner_name = models.CharField(max_length=100, default='')
    owner_contact = models.CharField(
        max_length=15, null=True, validators=[phone_validator])
    menu = models.FileField(upload_to='restaurant/menus/', null=True)
    business_plan = models.CharField(
        max_length=20, choices=BUSINESS_PLAN_CHOICES, null=True)
    restaurant_type = models.CharField(
        max_length=10, choices=RESTAURANT_TYPE_CHOICES, default='local')
    created_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.restaurant_name


class FoodItem(models.Model):
    AVAILABILITY_CHOICES = [
        ('OUT_OF_STOCK', 'Out of Stock'),
        ('LOW_STOCK', 'Low Stock'),
        ('AVAILABLE', 'Available'),
    ]
    
    VEG_NONVEG_CHOICES = [
        ('veg', 'Vegetarian'),
        ('nonveg', 'Non-Vegetarian'),
    ]

    RATING_CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    description = models.TextField(blank=True)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='food_items')
    veg_nonveg = models.CharField(max_length=6, choices=VEG_NONVEG_CHOICES, default='veg')
    profile_picture = models.ImageField(upload_to='food_images/', blank=True, null=True)
    external_image_url = models.URLField(blank=True, null=True)
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default='AVAILABLE'
    )
    review_rating = models.IntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True,
        help_text="Rate the food item from 0 to 5"
    )

    def __str__(self):
        return f"{self.name} - Rs. {self.price:.2f}"


class Deliveryman(models.Model):
    VEHICLE_CHOICES = [
        ('Scooter', 'Scooter'),
        ('Bike', 'Bike'),
    ]
    IDENTITY_CHOICES = [
        ('Citizenship', 'Citizenship'),
        ('Driving License', 'Driving License'),
    ]
    DELIVERY_TYPE_CHOICES = [
        ('Freelance', 'Freelancer'),
        ('Salarybased', 'Salarybased'),
    ]
    ZONE_CHOICES = [
        ('Kathmandu', 'Kathmandu'),
        ('Bhaktapur', 'Bhaktapur'),
        ('Lalitpur', 'Lalitpur'),
    ]
    DUTYTIME_CHOICES = [
        ('day', 'Day (10AM-6PM)'),
        ('night', 'Night (6PM-2AM)'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deliveryman_profile', null=True)
    Firstname = models.CharField(max_length=100)
    Lastname = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    DeliveryType = models.CharField(
        max_length=20, blank=False, choices=DELIVERY_TYPE_CHOICES)
    Zone = models.CharField(max_length=20, blank=False, choices=ZONE_CHOICES)
    Vehicle = models.CharField(
        max_length=20, blank=False, choices=VEHICLE_CHOICES)
    IdentityType = models.CharField(max_length=30, choices=IDENTITY_CHOICES, blank=False, null=True)
    IdentityNumber = models.CharField(max_length=30, blank=False)
    IdentityImage = models.ImageField(upload_to='identity_images/')
    PanNumber = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^\d{9}$',
                message='Enter a valid 9-digit PAN number'
            )
        ],
        help_text='Enter a 9-digit PAN number issued by IRD Nepal.'
    )
    BillBookScanCopy = models.ImageField(upload_to='bill_book_images/')
    DutyTime = models.CharField(
        max_length=10, blank=False, choices=DUTYTIME_CHOICES)
    VehicleNumber = models.CharField(
        max_length=13, 
        validators=[vehicle_validator], 
        help_text="Enter the vehicle number in capital letters (e.g., BA 2 PA 1234 or 3-01-Pa-1234).", 
        null=True
    )
    DateofBirth = models.DateField()
    UserImage = models.ImageField(upload_to='user_images/')
    created_at = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Firstname} {self.Lastname}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(
        'AppUser', 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    restaurant = models.ForeignKey(
        'Restaurant', 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    food_item = models.ForeignKey(
        'FoodItem', 
        on_delete=models.CASCADE, 
        related_name='orders',
        null=True, 
        blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Total price for this order",
        null=True, 
        blank=True  
    )
    is_transited = models.BooleanField(
        default=False,
        help_text="Whether the order is in transit/delivered"
    )
    deliveryman = models.ForeignKey(
        'Deliveryman', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='orders'
    )
    order_date = models.DateTimeField(default=timezone.now) 
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='PENDING'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-order_date']
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        if not self.total_price and self.food_item:
            self.total_price = self.food_item.price * self.quantity
  
        if self.status in ['OUT_FOR_DELIVERY', 'DELIVERED']:
            self.is_transited = True
        else:
            self.is_transited = False
        
        super().save(*args, **kwargs)
        
        # Update FoodOrderCount when new order is created
        if is_new and self.food_item:
            food_order_count, created = FoodOrderCount.objects.get_or_create(
                food_item=self.food_item
            )
            food_order_count.no_of_orders += self.quantity
            food_order_count.save()

    def calculate_total(self):
        if self.food_item:
            return self.food_item.price * self.quantity
        return 0

    def update_total_price(self):
        self.total_price = self.calculate_total()
        self.save(update_fields=['total_price'])

    def mark_as_transited(self):
        self.is_transited = True
        if self.status in ['PENDING', 'PROCESSING']:
            self.status = 'OUT_FOR_DELIVERY'
        self.save()

    def __str__(self):
        if self.food_item and self.user:
            return f"Order #{self.pk} - {self.food_item.name} x{self.quantity} by {self.user.name}"
        return f"Order #{self.pk}"


class FoodOrderCount(models.Model):
    food_item = models.OneToOneField(
        'FoodItem',
        on_delete=models.CASCADE, 
        related_name='order_count'
    )
    no_of_orders = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Food Order Count"
        verbose_name_plural = "Food Order Counts"

    def __str__(self):
        return f"{self.food_item.name} - {self.no_of_orders} orders"

    def increment_count(self, quantity=1):
        """Helper method to increment order count"""
        self.no_of_orders += quantity
        self.save(update_fields=['no_of_orders', 'updated_at'])

    def reset_count(self):
        """Helper method to reset order count"""
        self.no_of_orders = 0
        self.save(update_fields=['no_of_orders', 'updated_at'])


class DeliveryPersonnel(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=15, validators=[phone_validator])
    vehicle_type = models.CharField(max_length=50)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    current_order = models.OneToOneField(
        Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_personnel')
    deliveryman_profile = models.OneToOneField(
        'Deliveryman', on_delete=models.CASCADE, related_name='personnel_record', null=True)

    def __str__(self):
        status = f"Assigned to Order #{self.current_order.pk}" if self.current_order else "Available"
        return f"{self.name} - {status}"


class Delivery(models.Model):
    STATUS_CHOICES = [
        ('ASSIGNED', 'Assigned'),
        ('PICKED_UP', 'Picked Up'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'Failed'),
    ]

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='delivery')
    personnel = models.ForeignKey(
        DeliveryPersonnel, on_delete=models.SET_NULL, null=True, related_name='deliveries')
    delivery_address = models.TextField()
    assigned_time = models.DateTimeField(default=timezone.now)  # Fixed: use timezone.now
    delivery_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='ASSIGNED')

    def __str__(self):
        return f"Delivery #{self.pk} - Status: {self.status}"

    class Meta:
        verbose_name_plural = "Deliveries"


class DeliveryStatus(models.Model):
    STATUS_CHOICES = [
        ('ASSIGNED', 'Assigned'),
        ('PICKED_UP', 'Picked Up'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name='delivery_status')
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    deliveryman = models.ForeignKey(
        DeliveryPersonnel, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='ASSIGNED')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order.id} - {self.status}"