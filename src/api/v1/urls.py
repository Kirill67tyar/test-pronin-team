from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView

from api.v1.views import CollectModelViewSet, PaymentModelViewSet, RegisterAPIView

router_v1 = DefaultRouter()

router_v1.register("collections", CollectModelViewSet, basename="collection")
router_v1.register(
    r"collections/(?P<collect_id>\d+)/payments", PaymentModelViewSet, basename="payments"
)

urlpatterns_v1 = [
    path("", include(router_v1.urls)),
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/logout/", TokenBlacklistView.as_view(), name="logout"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refresh"),
    # path("api-auth/", include("rest_framework.urls")),
    # path('auth/', include('djoser.urls.authtoken')),
    # path('auth/', include('djoser.urls')),
    # # JWT-эндпоинты, для управления JWT-токенами:
    # path('auth/', include('djoser.urls.jwt')),
]
