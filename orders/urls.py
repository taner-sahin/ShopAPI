from rest_framework.routers import DefaultRouter

from .views import OrderItemViewSet, OrderViewSet

app_name = "orders"


router = DefaultRouter()

router.register(
    "orders",
    OrderViewSet,
    basename="order",
)

router.register(
    "order-items",
    OrderItemViewSet,
    basename="order-item",
)


urlpatterns = router.urls
