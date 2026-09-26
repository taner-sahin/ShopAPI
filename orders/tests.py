from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from products.models import Category, Product

from .models import Order, OrderItem

User = get_user_model()


class OrderAPITests(APITestCase):

    def setUp(self):
        # Kullanıcı 1
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="TestPassword123!",
        )

        # Kullanıcı 2
        self.other_user = User.objects.create_user(
            username="testuser2",
            email="testuser2@example.com",
            password="TestPassword123!",
        )

        # JWT access token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Category
        self.category = Category.objects.create(
            name="Electronics",
            slug="electronics",
        )

        # Product
        self.product = Product.objects.create(
            category=self.category,
            name="Mechanical Keyboard",
            description="Mechanical gaming keyboard",
            price="2499.90",
            stock=10,
            is_active=True,
        )

        # Kullanıcı 1'e ait Order
        self.order = Order.objects.create(
            user=self.user,
            status="pending",
        )

        # URL'ler
        self.order_list_url = reverse("orders:order-list")

        self.order_detail_url = reverse(
            "orders:order-detail",
            args=[self.order.id],
        )

        self.order_item_list_url = reverse("orders:order-item-list")

    def test_create_order_authenticated(self):
        response = self.client.post(
            self.order_list_url,
            {
                "status": "pending",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(Order.objects.count(), 2)

        created_order = Order.objects.latest("id")

        self.assertEqual(
            created_order.user,
            self.user,
        )

    def test_create_order_without_authentication(self):
        self.client.credentials()

        response = self.client.post(
            self.order_list_url,
            {
                "status": "pending",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.assertEqual(Order.objects.count(), 1)

    def test_user_can_view_own_order(self):
        response = self.client.get(self.order_detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            self.order.id,
        )

        self.assertEqual(
            response.data["user"],
            self.user.id,
        )

    def test_user_cannot_view_another_users_order(self):
        refresh = RefreshToken.for_user(self.other_user)

        other_access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=(f"Bearer {other_access_token}"))

        response = self.client.get(self.order_detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_create_order_item_for_own_order(self):
        response = self.client.post(
            self.order_item_list_url,
            {
                "order": self.order.id,
                "product": self.product.id,
                "quantity": 2,
                "price": "2499.90",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            OrderItem.objects.count(),
            1,
        )

        order_item = OrderItem.objects.first()

        self.assertEqual(
            order_item.order,
            self.order,
        )

        self.assertEqual(
            order_item.product,
            self.product,
        )

        self.assertEqual(
            order_item.quantity,
            2,
        )

    def test_user_cannot_add_item_to_another_users_order(self):
        refresh = RefreshToken.for_user(self.other_user)

        other_access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=(f"Bearer {other_access_token}"))

        response = self.client.post(
            self.order_item_list_url,
            {
                "order": self.order.id,
                "product": self.product.id,
                "quantity": 1,
                "price": "2499.90",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertEqual(
            OrderItem.objects.count(),
            0,
        )

    def test_order_detail_contains_items(self):
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price="2499.90",
        )

        response = self.client.get(self.order_detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data["items"]),
            1,
        )

        self.assertEqual(
            response.data["items"][0]["product"],
            self.product.id,
        )

        self.assertEqual(
            response.data["items"][0]["quantity"],
            2,
        )

    def test_user_only_sees_own_orders(self):
        Order.objects.create(
            user=self.other_user,
            status="pending",
        )

        response = self.client.get(self.order_list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["user"],
            self.user.id,
        )
