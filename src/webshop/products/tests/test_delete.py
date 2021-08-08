from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status


class ProductDeleteTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='testuser')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
        self.product_create()
        
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def product_create(self):
        request_json = {'sku': 101, 'name': 'Digital Watch', 'price': 450.99}
        self.client.post(path='/api/v1/products/', data=request_json)
        
    def test_product_delete_pass_detail_message(self):
        response = self.client.delete(path=f"/api/v1/products/101/")
        self.assertEqual(response.data['detail'], 'Product deleted.')

    def test_product_delete_pass_status_code(self):
        response = self.client.delete(path=f"/api/v1/products/101/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_delete_fail_detail_message(self):
        response = self.client.delete(path=f'/api/v1/products/102/')
        self.assertEqual(response.data['detail'], 'No Product matches the given query.')

    def test_product_delete_fail_status_code(self):
        response = self.client.delete(path=f"/api/v1/products/102/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
        # print(response.data['detail'])
