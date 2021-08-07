from re import S
from django.db.models import query
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from products.models import Product
from products.serializers import ProductsDetailsSerializer

class ProductsViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Product.objects.all()

    # raw_sql =  """
    # SELECT COUNT(DISTINCT wishlists_wishlist.owner_id) \
    #     FROM wishlists_wishlist \
    #     INNER JOIN wishlists_wishlist_products \
    #     ON wishlists_wishlist.id=wishlists_wishlist_products.id \
    #     WHERE wishlists_wishlist_products.product_id=883;"""

    def list(self, request):
        serializer_class = ProductsDetailsSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer_class = ProductsDetailsSerializer(product)
        return Response(serializer_class.data)

    def create(self, request):
        serializer = ProductsDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductsDetailsSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductsDetailsSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        product.delete()
        return Response(
            data = {"detail": "Product deleted."},
            status=status.HTTP_200_OK
            )

