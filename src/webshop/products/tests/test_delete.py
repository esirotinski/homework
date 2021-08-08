import random

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from products.models import Product

class ProductDeleteTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='testuser')
        cls.token = Token.objects.create(user=cls.user)
        cls.sku = random.getrandbits(32)
        cls.product = Product.objects.create(sku=cls.sku, name='Digital Watch', price=455.99)

    def setUp(self):
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
    def test_product_delete_passes(self):
        response = self.client.delete(path=f"/api/v1/products/{self.sku}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Product deleted.')

    def test_product_delete_fails(self):
        response = self.client.delete(path=f'/api/v1/products/102/')
        self.assertEqual(response.data['detail'], 'No Product matches the given query.')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
