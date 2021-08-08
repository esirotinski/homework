from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status


class ProductListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='testuser')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_product_list_authenticated(self):
        response = self.client.get(path='/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(f"{response.data = }")

    def test_product_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(path='/api/v1/products/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
