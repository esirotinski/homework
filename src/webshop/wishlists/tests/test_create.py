import random

from django.contrib.auth.models import User
from products.models import Product
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class WishlistCreateTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='testuser')
        cls.token = Token.objects.create(user=cls.user)
        cls.product1 = Product.objects.create(sku=random.getrandbits(32), name="name1", price=22.05)
        cls.product2 = Product.objects.create(sku=random.getrandbits(32), name="name2", price=42.05)


    def setUp(self):
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_wishlist_create_passes(self):
        request_json = {'name': 'Birthday Wishlist', 'products':[self.product2.sku, self.product1.sku]}
        response = self.client.post(path='/api/v1/wishlists/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], request_json['name'])

    def test_wishlist_create_no_products_fails(self):
        request_json = {'name': 'Birthday Wishlist', 'products':[]}
        response = self.client.post(path='/api/v1/wishlists/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['products'], ['This list may not be empty.'])

    def test_wishlist_create_fails(self):
        request_json = {'sku': 'demo', 'name': 'demouser'}
        response = self.client.post(path='/api/v1/wishlists/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['products'], ['This list may not be empty.'])
