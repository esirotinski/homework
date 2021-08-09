import random

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from products.models import Product


class WishlistPartialUpdateTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='testuser')
        cls.token = Token.objects.create(user=cls.user)
        cls.sku = random.getrandbits(32)
        cls.product = Product.objects.create(sku=cls.sku, name='Digital Watch', price=455.99)
        cls.wishlist_id = 0

    def setUp(self):
        self.api_authentication()
        self.create_wishlist()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
    def create_wishlist(self):
        request_json = {'name': 'Birthday Wishlist', 'products':[self.sku]}
        response = self.client.post(path='/api/v1/wishlists/', data=request_json)
        self.wishlist_id = response.json()['id']
    
    def test_wishlist_partial_update_passes(self):
        request_json = {'name': 'New Wishlist'}
        response = self.client.patch(path=f'/api/v1/wishlists/{self.wishlist_id}/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], 'New Wishlist')
    
    def test_wishlist_patial_update_fails(self):
        request_json = {'products':[]}
        response = self.client.patch(path=f'/api/v1/wishlists/{self.wishlist_id}/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['products'], [self.sku])
