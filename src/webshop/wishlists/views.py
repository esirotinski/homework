from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from webshop.permissions import IsOwnerOnly

from wishlists.models import Wishlist
from wishlists.serializers import WishlistsSerializer


class WishlistsViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsOwnerOnly)
    queryset = Wishlist.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def create(self, request):
        serializer = WishlistsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        serializer_class = WishlistsSerializer(self.get_queryset(), many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        wishlist = get_object_or_404(self.get_queryset(), pk=pk)
        serializer_class = WishlistsSerializer(wishlist)
        return Response(serializer_class.data)

    def update(self, request, pk=None):
        wishlist = get_object_or_404(self.queryset, pk=pk)
        serializer = WishlistsSerializer(wishlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        wishlist = get_object_or_404(self.queryset, pk=pk)
        serializer = WishlistsSerializer(wishlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        wishlist = get_object_or_404(self.queryset, pk=pk)
        wishlist.delete()
        return Response(data = {"detail": "Wishlist deleted."}, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def add_product(self, request, pk=None):
        """
        Adds a `Product` to the wishlist.
        """
        wishlist = get_object_or_404(self.queryset, pk=pk)
        serializer = WishlistsSerializer(wishlist, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                product_id = request.data['product']
                wishlist.products.add(product_id)
            except Exception:
                return Response(
                    data={"detail": f"Invalid pk \"{product_id}\" - object does not exist."}, 
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=True)
    def remove_product(self, request, pk=None):
        """
        Removes a `Product` from the wishlist.
        """
        wishlist = get_object_or_404(self.queryset, pk=pk)
        serializer = WishlistsSerializer(wishlist, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                product_id = request.data['product']
                wishlist.products.remove(product_id)
            except Exception:
                return Response(
                    data={"detail": f"Invalid pk \"{product_id}\" - object does not exist."}, 
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)
