import random

from django.contrib.auth.models import User
from rest_framework import response, status
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

    def test_product_retrieve_status_code_passes(self):
        response = self.client.get(path=f'/api/v1/products/{self.sku}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_retrieve_response_json_passes(self):
        response = self.client.get(path=f'/api/v1/products/{self.sku}/')
        self.assertEqual(response.json()['description'], None)
        self.assertEqual(response.json()['price'], '455.99')

    def test_product_retrieve_bad_sku_fails(self):
        response = self.client.get(path=f'/api/v1/products/101/')
        self.assertEqual(response.json()['detail'], 'Not found.')

    def test_product_retrieve_sku_chars_fails(self):
        response = self.client.get(path=f'/api/v1/products/abc/')
        self.assertEqual(response.json()['detail'], "Not found.")

    def test_product_retrieve_unauthenticated_fails(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(path=f'/api/v1/products/{self.sku}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
