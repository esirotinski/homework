import random

from django.contrib.auth.models import User
from products.models import Product
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from wishlists.models import Wishlist


class WishlistRetrieveTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='testuser')
        cls.user2 = User.objects.create_user(username='test2', password='testuser2')
        cls.token = Token.objects.create(user=cls.user)
        cls.token2 = Token.objects.create(user=cls.user2)
        cls.sku = random.getrandbits(32)
        cls.product = Product.objects.create(sku=cls.sku, name='Aee', price=202.99)
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

    def test_wishlist_retrieve_passes(self):
        response = self.client.get(path=f'/api/v1/wishlists/{self.wishlist_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wishlist_retrieve_unauthenticated_fails(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(path=f'/api/v1/wishlists/{self.wishlist_id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_wishlist_retrieve_authenticated_another_user_fails(self):
        self.client.force_authenticate(user=self.user2, token=self.token2)
        response = self.client.get(path=f'/api/v1/wishlists/{self.wishlist_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
