from rest_framework import serializers

from products.models import Product
from wishlists.models import Wishlist


class WishlistsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Wishlist
        fields = '__all__'


class WishlistsAddProductSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)

    class Meta:
        fields = ('product', )
        # fields = '__all__'