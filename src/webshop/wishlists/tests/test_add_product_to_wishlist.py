import random

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from products.models import Product
from wishlists.models import Wishlist


class WishlistAddProductTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='testuser')
        cls.token = Token.objects.create(user=cls.user)
        cls.sku = random.getrandbits(32)
        cls.sku2 = random.getrandbits(32)
        cls.product = Product.objects.create(sku=cls.sku, name='Digital Watch', price=455.99)
        cls.product2 = Product.objects.create(sku=cls.sku2, name='Smartphone', price=755.99)
        cls.wishlist_id = 0

    def setUp(self):
        self.api_authentication()
        self.create_wishlist()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        
    def create_wishlist(self):
        wishlist = Wishlist.objects.create(name='Birthday Wishlist', owner=self.user)
        wishlist.products.add(self.sku)
        self.wishlist_id = wishlist.id

    def test_wishlist_add_product_passes(self):
        request_json = {'product': f'{self.sku2}'}
        response = self.client.patch(path=f'/api/v1/wishlists/{self.wishlist_id}/add_product/', data=request_json)
        self.assertContains(response, self.sku, status_code=status.HTTP_200_OK)
        self.assertContains(response, self.sku2, status_code=status.HTTP_200_OK)
    
    def test_wishlist_add_product_fails(self):
        request_json = {'products': [101]}
        response = self.client.patch(path=f'/api/v1/wishlists/{self.wishlist_id}/add_product/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['product'], ['This field is required.'])
