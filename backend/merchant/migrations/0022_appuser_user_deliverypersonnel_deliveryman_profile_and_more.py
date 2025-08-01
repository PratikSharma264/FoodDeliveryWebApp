# Generated by Django 5.2 on 2025-07-23 11:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("merchant", "0021_deliveryman_approved_restaurant_approved"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="appuser",
            name="user",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="appuser_profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="deliverypersonnel",
            name="deliveryman_profile",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="personnel_record",
                to="merchant.deliveryman",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="deliveryman",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to="merchant.deliveryman",
            ),
        ),
        migrations.AlterField(
            model_name="deliveryman",
            name="Zone",
            field=models.CharField(
                choices=[
                    ("Kathmandu", "Kathmandu"),
                    ("Bhaktapur", "Bhaktapur"),
                    ("Lalitpur", "Lalitpur"),
                ],
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="DeliveryStatus",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ASSIGNED", "Assigned"),
                            ("PICKED_UP", "Picked Up"),
                            ("IN_TRANSIT", "In Transit"),
                            ("DELIVERED", "Delivered"),
                            ("FAILED", "Failed"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="ASSIGNED",
                        max_length=20,
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "deliveryman",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="merchant.deliverypersonnel",
                    ),
                ),
                (
                    "order",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="delivery_status",
                        to="merchant.order",
                    ),
                ),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="merchant.restaurant",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="merchant.appuser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MenuItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=7)),
                (
                    "discount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
                ),
                ("is_available", models.BooleanField(default=True)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="food_images/"),
                ),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="menu_items",
                        to="merchant.restaurant",
                    ),
                ),
            ],
        ),
    ]
