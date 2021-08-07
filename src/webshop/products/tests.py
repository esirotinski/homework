import json
from re import S
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import response, serializers, status
from products.models import Product
from products.serializers import ProductsDetailsSerializer


class ProtuctViewSetTestCase(APITestCase):

    def setUp(self):
        # return super().setUp()
        self.user = User.objects.create_user(username='test', password='testuser')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_product_creation_fails(self):
        data = {'username': 'demo', 'password': 'demouser'}
        response = self.client.post(path='/api/v1/products/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_creation_passes(self):
        data = {'sku': 101, 'name': 'Digital Watch', 'price': 450.99}
        response = self.client.post(path='/api/v1/products/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(f"{response.data = }")

    def test_product_list_authenticated(self):
        response = self.client.get(path='/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(f"{response.data = }")

    def test_product_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(path='/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print(f"{response.data = }")
