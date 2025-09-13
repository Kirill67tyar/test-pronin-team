from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from fees.models import Collect, Payment
from api.v1.serializers import (
    CollectDetailModelSerializer, 
    CollectListModelSerializer,
    CollectWriteModelSerializer, 
    PaymentDetailModelSerializer, 
    PaymentListModelSerializer, 
    PaymentWriteModelSerializer, 
    )
from django.db.models import Count, OuterRef, Subquery, Value, Sum
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import Coalesce, Concat
from django.contrib.postgres.fields import ArrayField
from django.db.models.fields import CharField
from decimal import Decimal


class PaymentModelViewSet(ModelViewSet):
    # queryset = Payment.objects.select_related("owner",)
    http_method_names = [
        "get",
        "post",
        "put",
        "delete",
    ]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PaymentDetailModelSerializer
        elif self.action == "list":
            return PaymentListModelSerializer
        return PaymentWriteModelSerializer
    
    def perform_create(self, serializer):
        collection = get_object_or_404(Collect, id=self.kwargs.get('collect_id'))
        serializer.save(collection=collection)
    
    def get_queryset(self):
        collection = get_object_or_404(Collect, id=self.kwargs.get('collect_id'))
        return collection.payments.select_related("owner", "collection").all()

class CollectModelViewSet(ModelViewSet):
    serializer_class = CollectDetailModelSerializer
    queryset = Collect.objects.select_related("author")
    # permission_classes = (IsAdminOrOwner,)
    http_method_names = [
        "get",
        "post",
        "put",
        "delete",
    ]
    def get_serializer_class(self):
        if self.action == 'list':
            return CollectListModelSerializer
        if self.action == 'retrieve':
            return CollectDetailModelSerializer
        return CollectWriteModelSerializer
        
    def get_queryset(self):
        current_amount_subquery = Subquery(
            Payment.objects.filter(collection=OuterRef('pk'))
            .values('collection')
            .annotate(total=Sum('amount'))
            .values('total')
        )
        queryset = super().get_queryset().annotate(
            current_amount=Coalesce(current_amount_subquery, Value(Decimal('0.00')))
            )
        if self.action == "retrieve":
            count_subquery = Subquery(
                Payment.objects.filter(collection=OuterRef('pk'))
                .values('collection')
                .annotate(count=Count('owner', distinct=True))
                .values('count')
            )

            names_subquery = Subquery(
                Payment.objects.filter(collection=OuterRef('pk'))
                .values('collection')
                .annotate(
                    full_names=ArrayAgg(
                        Concat('owner__first_name', Value(' '), 'owner__last_name', output_field=CharField()),
                        distinct=True
                    )
                )
                .values('full_names')
            )
            queryset = queryset.annotate(
                count_supporters=Coalesce(count_subquery, Value(0)),
                supporters_full_names=Coalesce(
                    names_subquery,
                    Value([], output_field=ArrayField(CharField()))
                ),
            )
        return queryset
