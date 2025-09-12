from rest_framework.viewsets import ModelViewSet
from fees.models import Collect, Payment
from api.v1.serializers import CollectModelSerializer, PaymentModelSerializer

class PaymentModelViewSet(ModelViewSet):
    serializer_class = PaymentModelSerializer
    queryset = Payment.objects.select_related("owner",)


class CollectModelViewSet(ModelViewSet):
    serializer_class = CollectModelSerializer
    queryset = Collect.objects.prefetch_related("payments", "payments__owner")
    # filter_backends = (SearchFilter,)
    # search_fields = ("username",)
    # permission_classes = (IsAdminOrOwner,)
    # lookup_field = "username"
    # lookup_url_kwarg = "username"
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
    ]
