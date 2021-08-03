from django.http import response
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from wishlists.models import Wishlist
from wishlists.serializers import WishlistDetailsSerializer


class WishlistsViewSet(viewsets.ViewSet):
    # permission_classes = (IsAuthenticated, )
    queryset = Wishlist.objects.all()

    def list(self, request):
        serializer_class = WishlistDetailsSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        wishlist = get_object_or_404(self.queryset, pk=pk)
        serializer_class = WishlistDetailsSerializer(wishlist)
        return Response(serializer_class.data)

    def create(self, request):
        serializer = WishlistDetailsSerializer(data=request.data)

        if serializer.is_valid():
            # name = serializer.data.get('name')
            # owner = serializer.data.get('owner')
            # products = serializer.data.get('products')
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        wishlist = get_object_or_404(self.queryset, pk=pk)
        wishlist.delete()
        return Response(
            # response_data = {"detail":"Item deleted."}
            # data = '' , # Would be nice to add response json with details.
            status=status.HTTP_204_NO_CONTENT
            )
