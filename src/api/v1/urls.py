from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import CollectModelViewSet, PaymentModelViewSet

router_v1 = DefaultRouter()

router_v1.register("collections", CollectModelViewSet, basename="collection")
router_v1.register(
    r"collections/(?P<collect_id>\d+)/payments", PaymentModelViewSet, basename="payments"
)

urlpatterns_v1 = [
    path("", include(router_v1.urls)),
]
