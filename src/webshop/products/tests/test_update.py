import random

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Product

class ProductCreateTestCase(APITestCase):

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

    def test_product_update_passes(self):
        request_json = {'sku': self.sku, 'name': 'Smart Watch', 'price': 450.99}
        response = self.client.put(path=f'/api/v1/products/{self.sku}/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], request_json['name'])

    def test_product_update_fails(self):
        request_json = {'sku': 'demo', 'name': 'demouser'}
        response = self.client.put(path=f'/api/v1/products/{self.sku}/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['sku'], ['A valid integer is required.'])
        self.assertEqual(response.json()['price'], ['This field is required.'])
