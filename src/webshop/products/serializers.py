from django.db import models
from rest_framework import serializers
from products.models import Product


class ProductsDetailsSerializer(serializers.ModelSerializer):
    wished_counter = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ('wished_counter', 'sku', 'name', 'price')


