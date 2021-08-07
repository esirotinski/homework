from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Product(models.Model):
    sku = models.PositiveIntegerField(
        primary_key=True,
        unique=True,
        blank=False,
        null=False)
    name = models.CharField(max_length=64, blank=False, null=False)
    price = models.DecimalField(
        blank=False,
        null=False,
        max_digits=8,
        decimal_places=2)
    description = models.TextField(
        max_length=512,
        blank=True,
        null=True)
    # wished_counter = models.BigIntegerField(
    #     verbose_name="Wished by unique users counter",
    #     default=0)
    # owner = models.ForeignKey(
    #     User, 
    #     on_delete=models.CASCADE,
    #     blank=False,
    #     null=False)

    def __str__(self):
        return f"SKU {str(self.sku)}"
