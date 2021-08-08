import random

from django.contrib.auth.models import User
from rest_framework import request, response, status
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

    def test_product_partial_updated_passes(self):
        request_json = {'name': 'Smartphone'}
        response = self.client.patch(path=f'/api/v1/products/{self.sku}/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'Smartphone')

    def test_product_partial_update_fails(self):
        request_json = {'name': ''}
        response = self.client.patch(path=f'/api/v1/products/{self.sku}/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['name'], ['This field may not be blank.'])

    def test_product_partial_update_with_random_data_passes(self):
        request_json = {'random': 'bla'}
        response = self.client.patch(path=f'/api/v1/products/{self.sku}/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['price'], '455.99')
