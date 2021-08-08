from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Product(models.Model):
    sku = models.PositiveIntegerField(
        primary_key=True,
        unique=True,
        blank=False,
        null=False)
    name = models.CharField(
        max_length=64,
        blank=False,
        null=False)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=False,
        null=False)
    description = models.CharField(
        max_length=512,
        blank=True,
        null=True)

    def __str__(self):
        return f"SKU {str(self.sku)}"
