from rest_framework import serializers
from products.models import Product


class ProductRetrieveSerializer(serializers.ModelSerializer):
    uniq_users_who_wished_this_product = serializers.IntegerField(default=0)
    class Meta:
        model = Product
        fields = ('sku', 'name', 'price', 'uniq_users_who_wished_this_product')


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('sku', 'name', 'price')
