from django.db import models
from rest_framework import serializers
from products.models import Product


class ProductsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
