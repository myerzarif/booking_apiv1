"""Account Test Module"""
import json
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User
import json


class AccountTest(TestCase):
    """Test Account Model, View, ..."""

    @override_settings(RATELIMIT_ENABLE=False)
    def setUp(self):
        self.register_data = {
            "email": "test1@email.test",
            "password": "123456",
            "confirm_password": "123456"
        }
        self.login_data = {
            "email": "test1@email.test",
            "password": "123456"
        }

    @override_settings(RATELIMIT_ENABLE=False)
    def test_001_register_user(self):
        """
        Register User
        """
        client = Client()
        response = client.post(
            reverse('account:register'), data=self.register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_obj = User.objects.get(email='test1@email.test')
        self.assertEqual(user_obj.email, self.register_data['email'])

    @override_settings(RATELIMIT_ENABLE=False)
    def test_002_register_user_failed(self):
        """
        Register user - failed scenarios
        """
        client = Client()
        response = client.post(reverse('account:register'),
                               data={**self.register_data, 'email': 'asndidu'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = client.post(reverse('account:register'),
                               data={**self.register_data, "password": "!123qwE@pss", "confirm_password": "123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = client.post(reverse('account:register'),
                               data={**self.register_data, "password": "123", "confirm_password": "123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(RATELIMIT_ENABLE=False)
    def test_003_login_success(self):
        """
        Successfull login 
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)

        response = client.post(reverse('account:login'), data=self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(RATELIMIT_ENABLE=False)
    def test_004_login_failed(self):
        """
        Failed login
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)

        response = client.post(reverse('account:login'), data={
                               'email': 'a@b.com', "password": "123456"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = client.post(reverse('account:login'), data={
                               'email': 'test1@email.test', "password": "123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(RATELIMIT_ENABLE=False)
    def test_005_get_user_authorized(self):
        """
        Get user with authorize client
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)
        response = client.post(reverse('account:login'), data=self.login_data)
        token = response.json()['access_token']
        user_id = token.get("user", {}).get("id")
        key = token.get("key")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {key}")
        response = client.get(reverse('account:user', kwargs={'pk': user_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(RATELIMIT_ENABLE=False)
    def test_006_get_user_unauthorized(self):
        """
        Get user with unauthorize client
        """
        client = Client()
        response = client.post(reverse('account:register'), data=self.register_data)
        user_id = response.json()['id']
        response = client.get(reverse('account:user', kwargs={'pk': user_id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
