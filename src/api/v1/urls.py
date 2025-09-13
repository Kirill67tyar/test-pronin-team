from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    PaymentModelViewSet,
    CollectModelViewSet,
)

router_v1 = DefaultRouter()

router_v1.register("collections", CollectModelViewSet, basename="collection")
# router_v1.register("payments", PaymentModelViewSet, basename="payment")
router_v1.register(
    r'collections/(?P<collect_id>\d+)/payments', PaymentModelViewSet, basename='payments'
)
# router_v1.register("categories", CategoryViewSet, basename="categorie")
# router_v1.register(
#     r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
# )
# router_v1.register(
#     r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
#     CommentViewSet,
#     basename="comments",
# )
# router_v1.register(r"users", UserModelViewSet, basename="users")

urlpatterns_v1 = [
    path("", include(router_v1.urls)),
    # path("auth/signup/", register_user_view, name="signup"),
    # path("auth/token/", get_token_view, name="token_obtain_pair"),
]