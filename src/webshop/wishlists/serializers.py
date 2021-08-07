from rest_framework import serializers
from wishlists.models import Wishlist


class WishlistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'
