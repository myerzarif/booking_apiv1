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
            "address": "Address 1 Address 1 Address 1",
            "password": "Test123456$",
            "confirm_password": "Test123456$",
        }

        self.login_data = {
            "username": "test1@email.test",
            "password": "Test123456$",
        }

        self.change_pass_data = {
            "email": "test1@email.test",
            "old_password": "Test123456$",
            "new_password": "Test12345678",
            "confirm_password": "Test12345678",
        }

        self.send_token_data = {
            "username": "test1@email.test",
        }

        self.reset_password_data = {
            "username_base64": "dGVzdDFAZW1haWwudGVzdA==",
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "token": "tt",
            "new_password": "Test12345678",
            "confirm_password": "Test12345678",
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
                               data={**self.register_data, 'address': '1234'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = client.post(reverse('account:register'),
                               data={**self.register_data, "password": "!123qwE@pss", "confirm_password": "123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = client.post(reverse('account:register'),
                               data={**self.register_data, "password": "123", "confirm_password": "123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = client.post(reverse('account:register'),
                               data={**self.register_data, "password": "123456", "confirm_password": "123456"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(RATELIMIT_ENABLE=False)
    def test_003_login_success(self):
        """
        Successful login 
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)
        user_obj = User.objects.get(email='test1@email.test')
        # user_obj.email_verified = True
        user_obj.status = User.UserStatus.ACTIVE
        user_obj.save()
        response = client.post(reverse('account:login'), data=self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(RATELIMIT_ENABLE=False)
    def test_004_login_failed(self):
        """
        Failed login
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)
        #not verified email
        response = client.post(reverse('account:login'), data=self.login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_obj = User.objects.get(email='test1@email.test')
        # user_obj.email_verified = True
        user_obj.status = User.UserStatus.ACTIVE
        user_obj.save()

        response = client.post(reverse('account:login'), data={
                               'username': 'a@b.com', "password": "Test123456$"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        response = client.post(reverse('account:login'), data={
                               'username': 'test1@email.test', "password": "123"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(RATELIMIT_ENABLE=False)
    def test_005_get_user_authorized(self):
        """
        Get user with authorize client
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)
        user_obj = User.objects.get(email='test1@email.test')
        # user_obj.email_verified = True
        user_obj.status = User.UserStatus.ACTIVE
        user_obj.role = User.UserRole.TECH
        user_obj.save()
        response = client.post(reverse('account:login'), data=self.login_data)
        token = response.json()['data']
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
        response = client.post(
            reverse('account:register'), data=self.register_data)
        user_id = response.json()['data']['id']
        response = client.get(reverse('account:user', kwargs={'pk': user_id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(RATELIMIT_ENABLE=False)
    def test_007_change_password_success(self):
        """
        Successful change password 
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)
        user_obj = User.objects.get(email='test1@email.test')
        # user_obj.email_verified = True
        user_obj.status = User.UserStatus.ACTIVE
        user_obj.save()

        response = client.post(reverse('account:login'), data=self.login_data)
        token = response.json()['data']
        key = token.get("key")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {key}")

        response = client.post(reverse('account:change_password'), data=self.change_pass_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    @override_settings(RATELIMIT_ENABLE=False)
    def test_008_change_password_success(self):
        """
        Successful change password empty confirm password
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)
        user_obj = User.objects.get(email='test1@email.test')
        # user_obj.email_verified = True
        user_obj.status = User.UserStatus.ACTIVE
        user_obj.save()

        client2 = Client()
        response2 = client2.post(reverse('account:login'), data=self.login_data)
        token = response2.json()['data']
        key = token.get("key")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {key}")
        data = {
            "email": "test1@email.test",
            "old_password": "Test123456$",
            "new_password": "Test12345678",
        }

        response = client.post(reverse('account:change_password'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(RATELIMIT_ENABLE=False)
    def test_009_change_password_success(self):
        """
        Successful change password empty email but check with logged in user
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)
        user_obj = User.objects.get(email='test1@email.test')
        # user_obj.email_verified = True
        user_obj.status = User.UserStatus.ACTIVE
        user_obj.save()

        client2 = Client()
        response2 = client2.post(reverse('account:login'), data=self.login_data)
        token = response2.json()['data']
        key = token.get("key")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {key}")
        data = {
            "old_password": "Test123456$",
            "new_password": "Test12345678",
            "confirm_password": "Test12345678",
        }
        response = client.post(reverse('account:change_password'), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(RATELIMIT_ENABLE=False)
    def test_010_change_password_failure(self):
        """
        Failure change password
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)
        user_obj = User.objects.get(email='test1@email.test')
        # user_obj.email_verified = True
        user_obj.status = User.UserStatus.ACTIVE
        user_obj.save()

        #Not logged in
        response = client.post(reverse('account:change_password'), data=self.change_pass_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client2 = Client()
        response2 = client2.post(reverse('account:login'), data=self.login_data)
        token = response2.json()['data']
        key = token.get("key")
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {key}")

        #change password of other user
        data = {
            "email": "test2@email.test",
            "old_password": "Test123456%",
            "new_password": "Test12345678",
            "confirm_password": "Test12345678",
        }
        response = client.post(reverse('account:change_password'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #change password to weak password
        data = {
            "email": "test2@email.test",
            "old_password": "Test123456%",
            "new_password": "12345678",
            "confirm_password": "12345678",
        }
        response = client.post(reverse('account:change_password'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #change password with wrong confirm
        data = {
            "email": "test2@email.test",
            "old_password": "Test123456%",
            "new_password": "Test12345678",
            "confirm_password": "Test123456789",
        }
        response = client.post(reverse('account:change_password'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #change password with wrong old pass
        data = {
            "email": "test2@email.test",
            "old_password": "Test12345",
            "new_password": "Test12345678",
            "confirm_password": "Test12345678",
        }
        response = client.post(reverse('account:change_password'), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #empty request
        response = client.post(reverse('account:change_password'), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @override_settings(RATELIMIT_ENABLE=False)
    def test_011_send_reset_password_token_success(self):
        """
        Successful send reset password token
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)
        user_obj = User.objects.get(email='test1@email.test')
        # user_obj.email_verified = True
        user_obj.status = User.UserStatus.ACTIVE
        user_obj.save()

        response = client.post(reverse('account:send_reset_password_token'), data=self.send_token_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @override_settings(RATELIMIT_ENABLE=False)
    def test_012_send_reset_password_token_failure(self):
        """
        Fail send reset password token
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)
        user_obj = User.objects.get(email='test1@email.test')
        # user_obj.email_verified = True
        user_obj.status = User.UserStatus.ACTIVE
        user_obj.save()

        #empty request
        response = client.post(reverse('account:send_reset_password_token'), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #wrong email
        response = client.post(reverse('account:send_reset_password_token'), data={'username':'test@test.com'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    @override_settings(RATELIMIT_ENABLE=False)
    def test_013_reset_password_success(self):
        """
        Successful reset password
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)
        user_obj = User.objects.get(email='test1@email.test')
        # user_obj.email_verified = True
        user_obj.status = User.UserStatus.ACTIVE
        user_obj.save()

        response = client.post(reverse('account:get_password_token'), data=self.send_token_data)
        token = response.json()['data']['token']
        user_id = response.json()['data']['user_id']
        reset_password_data = self.reset_password_data
        reset_password_data['token']=token
        reset_password_data['user_id']=user_id
        response = client.post(reverse('account:reset_password'), data=reset_password_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(RATELIMIT_ENABLE=False)
    def test_014_reset_password_failure(self):
        """
        Fail reset password
        """
        client = Client()
        client.post(reverse('account:register'), data=self.register_data)
        user_obj = User.objects.get(email='test1@email.test')
        # user_obj.email_verified = True
        user_obj.status = User.UserStatus.ACTIVE
        user_obj.save()
        self.reset_password_data['user_id'] = user_obj.id
        #empty request
        response = client.post(reverse('account:reset_password'), data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #wrong token
        response = client.post(reverse('account:reset_password'), data=self.reset_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #wrong confirm
        reset_password_data = self.reset_password_data
        reset_password_data['confirm_password']='test'
        response = client.post(reverse('account:reset_password'), data=reset_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #weak password
        reset_password_data = self.reset_password_data
        reset_password_data['confirm_password']='test'
        reset_password_data['new_password']='test'
        response = client.post(reverse('account:reset_password'), data=reset_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #wrong email
        reset_password_data = self.reset_password_data
        reset_password_data['email']='test@test.com'
        response = client.post(reverse('account:reset_password'), data=reset_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #wrong username encode
        reset_password_data = self.reset_password_data
        reset_password_data["user_id"] = "dGVzdEBlbWFpbC50ZXN0",
        response = client.post(reverse('account:reset_password'), data=reset_password_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)