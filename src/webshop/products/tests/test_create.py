from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status


class ProductCreateTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='testuser')
        cls.token = Token.objects.create(user=cls.user)

    def setUp(self):
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_product_create_passes(self):
        request_json = {'sku': 101, 'name': 'Digital Watch', 'price': 450.99}
        response = self.client.post(path='/api/v1/products/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sku'], request_json['sku'])

    def test_product_create_fails(self):
        request_json = {'sku': 'demo', 'name': 'demouser'}
        response = self.client.post(path='/api/v1/products/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['sku'], ['A valid integer is required.'])
        self.assertEqual(response.json()['price'], ['This field is required.'])
