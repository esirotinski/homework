from django.db.models import Count
from rest_framework import serializers
from products.models import Product


class ProductRetrieveSerializer(serializers.ModelSerializer):
    users_count = serializers.SerializerMethodField()

    def get_users_count(self, obj):
        return Product.objects.filter(sku=obj.pk).annotate(count=Count('wishlist__owner', distinct=True)).first().count

    class Meta:
        model = Product
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
