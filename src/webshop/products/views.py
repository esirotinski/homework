from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from products.models import Product
from products.serializers import ProductsSerializer, ProductRetrieveSerializer

class ProductsViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = Product.objects.all()

    def create(self, request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        serializer_class = ProductsSerializer(self.queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        try:
            product = get_object_or_404(self.queryset, pk=pk)
        except Http404 as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            sql_query = Product.objects.raw(
                f"""
                SELECT products_product.sku as sku,
                    (SELECT COUNT(distinct wishlists_wishlist.owner_id)
                FROM wishlists_wishlist
                INNER JOIN wishlists_wishlist_products
                ON wishlists_wishlist.id=wishlists_wishlist_products.wishlist_id
                WHERE wishlists_wishlist_products.product_id={pk}) AS uniq_users
                FROM products_product where products_product.sku={pk}
                """)
            # psql_query = Product.objects.raw(
            #     f"""
            #     SELECT products_product.sku as sku,
            #       (SELECT COUNT(distinct wishlists_wishlist.owner_id) AS uniq_users
            #     FROM wishlists_wishlist
            #     INNER JOIN wishlists_wishlist_products
            #     ON wishlists_wishlist.id=wishlists_wishlist_products.wishlist_id
            #     WHERE wishlists_wishlist_products.product_id={pk})
            #     FROM products_product where products_product.sku={pk}
            #     """
            # )
            product.uniq_users_who_wished_this_product = sql_query[0].uniq_users
            serializer_class = ProductRetrieveSerializer(product)
            return Response(serializer_class.data)

    def update(self, request, pk=None):
        try:
            product = get_object_or_404(self.queryset, pk=pk)
            serializer = ProductsSerializer(product, data=request.data)
        except Http404 as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            product = get_object_or_404(self.queryset, pk=pk)
            serializer = ProductsSerializer(product, data=request.data, partial=True)
        except Http404 as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            product = get_object_or_404(self.queryset, pk=pk)
            product.delete()
        except Http404 as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data = {"detail": "Product deleted."}, status=status.HTTP_200_OK)
