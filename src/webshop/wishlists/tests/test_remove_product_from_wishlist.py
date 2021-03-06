import random

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from products.models import Product
from wishlists.models import Wishlist


class WishlistRemoveProductTestCase(APITestCase):

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
    
    def test_wishlist_remove_product_passes(self):
        request_json = {'product': f'{self.sku2}'}
        response = self.client.patch(path=f'/api/v1/wishlists/{self.wishlist_id}/remove_product/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['products'], [self.sku])
    
    def test_wishlist_remove_product_fails(self):
        request_json = {'products': [101]}
        response = self.client.patch(path=f'/api/v1/wishlists/{self.wishlist_id}/remove_product/', data=request_json)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # TODO: Fix code here: 
        # print(response.json()['detail'])
        # Traceback (most recent call last):
        #   File "/home/sh/git/homework/src/webshop/wishlists/tests/test_remove_product_from_wishlist.py", line 44, in test_wishlist_remove_product_fails
        #     print(response.json()['detail'])
        # TypeError: string indices must be integers

        # ----------------------------------------------------------------------
        # self.assertEqual(response.json()[0], "{'detail':'Unexpected data. JSON should contain `product` with valid `id`.'}")
        #
        # Traceback (most recent call last):
        #   File "/home/sh/git/homework/src/webshop/wishlists/tests/test_add_product_to_wishlist.py", line 48, in test_wishlist_add_product_fails
        #     self.assertEqual(response.json()[0], "{'detail':'Unexpected data. JSON should contain `product` with valid `id`.'}")
        # AssertionError: '{' != "{'detail':'Unexpected data. JSON should contain `product` with valid `id`.'}"
        # - {
        # + {'detail':'Unexpected data. JSON should contain `product` with valid `id`.'}
