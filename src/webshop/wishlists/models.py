from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product


User = get_user_model()

class Wishlist(models.Model):
    name = models.CharField(
        max_length=64,
        blank=False,
        null=False)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name
