from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status


class ProductCreateTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='testuser')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_product_create_passes(self):
        request_json = {'sku': 101, 'name': 'Digital Watch', 'price': 450.99}
        response = self.client.post(path='/api/v1/products/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sku'], request_json['sku'])

    def test_product_create_fails(self):
        request_json = {'username': 'demo', 'password': 'demouser'}
        response = self.client.post(path='/api/v1/products/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
