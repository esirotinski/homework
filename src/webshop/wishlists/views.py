from django.http.response import Http404
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from webshop.permissions import IsOwnerOnly

from wishlists.models import Wishlist
from wishlists.serializers import WishlistsSerializer, WishlistsAddProductSerializer


class WishlistsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOnly)
    queryset = Wishlist.objects.all()
    serializer_class = WishlistsSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    @action(methods=['patch'], detail=True)
    @swagger_auto_schema(request_body=WishlistsAddProductSerializer)
    def add_product(self, request, pk=None):
        """
        Adds a `Product` to the wishlist.
        """
        wishlist = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = WishlistsAddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wishlist.products.add(serializer.validated_data.get('product'))
        return Response(WishlistsSerializer(wishlist).data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    @swagger_auto_schema(request_body=WishlistsAddProductSerializer)
    def remove_product(self, request, pk=None):
        """
        Removes a `Product` from the wishlist.
        """
        wishlist = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = WishlistsAddProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wishlist.products.remove(serializer.validated_data.get('product'))
        return Response(WishlistsSerializer(wishlist).data, status=status.HTTP_200_OK)
