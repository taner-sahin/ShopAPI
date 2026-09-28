from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product

User = get_user_model()


class ProductAPITests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

        self.product = Product.objects.create(
            category=self.category,
            name="Mechanical Keyboard",
            description="Mechanical gaming keyboard",
            price="2499.90",
            stock=10,
            is_active=True,
        )

        self.normal_user = User.objects.create_user(
            username="normaluser",
            password="TestPassword123!",
        )

        self.staff_user = User.objects.create_user(
            username="staffuser",
            password="TestPassword123!",
            is_staff=True,
        )

        self.product_list_url = reverse("products:product-list")
        self.product_detail_url = reverse(
            "products:product-detail",
            args=[self.product.id],
        )

    def test_product_list(self):
        response = self.client.get(self.product_list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["name"],
            "Mechanical Keyboard",
        )

    def test_product_detail(self):
        response = self.client.get(self.product_detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["name"],
            "Mechanical Keyboard",
        )
        self.assertEqual(
            response.data["stock"],
            10,
        )

    def test_staff_user_can_create_product(self):
        self.client.force_authenticate(
            user=self.staff_user,
        )

        data = {
            "category": self.category.id,
            "name": "Gaming Mouse",
            "description": "Wireless gaming mouse",
            "price": "1499.90",
            "stock": 20,
            "is_active": True,
        }

        response = self.client.post(
            self.product_list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Product.objects.count(),
            2,
        )
        self.assertTrue(
            Product.objects.filter(
                name="Gaming Mouse",
            ).exists()
        )

    def test_normal_user_cannot_create_product(self):
        self.client.force_authenticate(
            user=self.normal_user,
        )

        data = {
            "category": self.category.id,
            "name": "Gaming Mouse",
            "description": "Wireless gaming mouse",
            "price": "1499.90",
            "stock": 20,
            "is_active": True,
        }

        response = self.client.post(
            self.product_list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertEqual(
            Product.objects.count(),
            1,
        )

    def test_staff_user_can_update_product_with_patch(self):
        self.client.force_authenticate(
            user=self.staff_user,
        )

        data = {
            "stock": 35,
        }

        response = self.client.patch(
            self.product_detail_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock,
            35,
        )
        self.assertEqual(
            self.product.name,
            "Mechanical Keyboard",
        )

    def test_normal_user_cannot_update_product(self):
        self.client.force_authenticate(
            user=self.normal_user,
        )

        data = {
            "stock": 999,
        }

        response = self.client.patch(
            self.product_detail_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock,
            10,
        )

    def test_staff_user_can_delete_product(self):
        self.client.force_authenticate(
            user=self.staff_user,
        )

        response = self.client.delete(
            self.product_detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Product.objects.filter(
                id=self.product.id,
            ).exists()
        )

    def test_normal_user_cannot_delete_product(self):
        self.client.force_authenticate(
            user=self.normal_user,
        )

        response = self.client.delete(
            self.product_detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )
        self.assertTrue(
            Product.objects.filter(
                id=self.product.id,
            ).exists()
        )

    def test_product_not_found(self):
        url = reverse(
            "products:product-detail",
            args=[99999],
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_staff_user_cannot_create_product_with_invalid_data(self):
        self.client.force_authenticate(
            user=self.staff_user,
        )

        data = {
            "name": "",
        }

        response = self.client.post(
            self.product_list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "category",
            response.data,
        )
        self.assertIn(
            "name",
            response.data,
        )
        self.assertIn(
            "price",
            response.data,
        )

        self.assertEqual(
            Product.objects.count(),
            1,
        )
