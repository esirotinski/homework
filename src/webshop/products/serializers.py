from rest_framework import serializers
from products.models import Product


class ProductRetrieveSerializer(serializers.ModelSerializer):
    uniq_users_who_wished_this_product = serializers.IntegerField()
    class Meta:
        model = Product
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
