import random

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from products.models import Product


class WishlistDeleteTestCase(APITestCase):

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
    
    def test_wishlist_delete_passes(self):
        response = self.client.delete(path=f"/api/v1/wishlists/{self.wishlist_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_wishlist_delete_fails(self):
        response = self.client.delete(path=f'/api/v1/wishlists/102/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['detail'], 'Not found.')
