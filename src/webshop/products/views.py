from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from products.models import Product
from products.serializers import ProductsSerializer, ProductRetrieveSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductRetrieveSerializer
        return super().get_serializer_class()
