from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="Testpass123",
        )

        self.register_url = reverse("users:register")
        self.token_url = reverse("users:token_obtain_pair")
        self.refresh_url = reverse("users:token_refresh")
        self.profile_url = reverse("users:profile")

    def test_register_user(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Newpass123",
        }

        response = self.client.post(
            self.register_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(User.objects.filter(username="newuser").exists())

        user = User.objects.get(username="newuser")

        self.assertTrue(user.check_password("Newpass123"))

        self.assertNotIn("password", response.data)

    def test_register_with_short_password(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "123",
        }

        response = self.client.post(
            self.register_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn("password", response.data)

        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_obtain_token(self):
        data = {
            "username": "testuser",
            "password": "Testpass123",
        }

        response = self.client.post(
            self.token_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_obtain_token_with_wrong_password(self):
        data = {
            "username": "testuser",
            "password": "WrongPassword123",
        }

        response = self.client.post(
            self.token_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_refresh_token(self):
        token_response = self.client.post(
            self.token_url,
            {
                "username": "testuser",
                "password": "Testpass123",
            },
            format="json",
        )

        refresh_token = token_response.data["refresh"]

        response = self.client.post(
            self.refresh_url,
            {
                "refresh": refresh_token,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)

    def test_profile_without_authentication(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_profile_with_valid_access_token(self):
        token_response = self.client.post(
            self.token_url,
            {
                "username": "testuser",
                "password": "Testpass123",
            },
            format="json",
        )

        access_token = token_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get(self.profile_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["username"],
            "testuser",
        )

        self.assertEqual(
            response.data["email"],
            "testuser@example.com",
        )

    def test_profile_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid-token")

        response = self.client.get(self.profile_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
