import random

from django.contrib.auth.models import User
from products.models import Product
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class ProductListTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='testuser')
        cls.token = Token.objects.create(user=cls.user)
        cls.product = Product.objects.create(sku=random.getrandbits(32), name='Aee', price=202.99)

    def setUp(self):
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_product_list_authenticated_passes(self):
        response = self.client.get(path='/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_product_list_unauthenticated_fails(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(path='/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
