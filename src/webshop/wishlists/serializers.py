from rest_framework import serializers
from wishlists.models import Wishlist


class WishlistsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Wishlist
        fields = '__all__'
