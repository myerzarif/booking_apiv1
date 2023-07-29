from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient
from config.settings import BASE_DIR
from .models import File
from account.models import User
import json

class TestFile(TestCase):
    def setUp(self):
        self.register_data = {
            "email": "test1@email.test",
            "address": "Address 1 Address 1 Address 1",
            "password": "aA12345678$",
            "confirm_password": "aA12345678$"
        }
        self.login_data = {
            "username": "test1@email.test",
            "password": "aA12345678$"
        }
        client = Client()
        register_response = client.post(
            reverse('account:register'), data=self.register_data)
        self.user = register_response.json()
        user_obj = User.objects.get(email='test1@email.test')
        # user_obj.email_verified = True
        user_obj.status = User.UserStatus.ACTIVE
        user_obj.save()
        response = client.post(reverse('account:login'), data=self.login_data)
        self.token = response.json()['data']

    def test_001_upload_file_test(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION="Token {}".format(self.token.get("key")))
        with open(BASE_DIR / 'tests' / 'png-test.png', 'rb') as data:
            response = client.post(reverse('file:upload'), data={'file': data})
            self.assertEqual(response.status_code, 201)
            file = File.objects.last()
            self.assertEqual(response.data["file"]["id"], file.id.__str__())
            self.assertEqual(response.data["file"]["file_format"], file.format)