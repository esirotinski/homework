from rest_framework import serializers
from wishlists.models import Wishlist


class WishlistDetailsSerializer(serializers.ModelSerializer):
    # owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Wishlist
        fields = '__all__'
        # fields = ['name', 'owner', 'products']

