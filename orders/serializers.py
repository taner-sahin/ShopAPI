from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "quantity",
            "price",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "status",
            "items",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "user",
            "created_at",
            "updated_at",
        )
