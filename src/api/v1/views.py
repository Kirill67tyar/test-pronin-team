from rest_framework.response import Response
from django.core.cache import cache
from django.db import transaction
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
from fees.tasks import send_email_task
from fees.utils import build_payment_email, build_collect_email
# from rest_framework.pagination import PageNumberPagination
from django.conf import settings

class PaymentModelViewSet(ModelViewSet):
    # queryset = Payment.objects.select_related("owner",)
    # pagination_class = PageNumberPagination
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
        instance = serializer.save(collection=collection)
        # if self.request.user.email is not None:
        if instance.owner.email is not None:
            subject, message, recipient_list, html_message = build_payment_email(
                owner_name=instance.owner.first_name,
                owner_email=instance.owner.email,
                amount=instance.amount,
                collect_name=instance.collection.name
            )
            transaction.on_commit(
                lambda: send_email_task.delay(subject, message, recipient_list, html_message)
            )
    
    def get_queryset(self):
        collection = get_object_or_404(Collect, id=self.kwargs.get('collect_id'))
        return collection.payments.select_related("owner", "collection").all()

class CollectModelViewSet(ModelViewSet):
    serializer_class = CollectDetailModelSerializer
    queryset = Collect.objects.select_related("author")
    # pagination_class = PageNumberPagination
    # permission_classes = (IsAdminOrOwner,)
    http_method_names = [
        "get",
        "post",
        "put",
        "delete",
    ]
    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.author.email is not None:
            subject, message, recipient_list, html_message = build_collect_email(
                author_name=instance.author.first_name,
                author_email=instance.author.email,
                planned_amount=instance.planned_amount,
                collect_name=instance.name
                )
            transaction.on_commit(
                lambda: send_email_task.delay(subject, message, recipient_list, html_message)
            )

    def get_serializer_class(self):
        if self.action == 'list':
            return CollectListModelSerializer
        if self.action == 'retrieve':
            return CollectDetailModelSerializer
        return CollectWriteModelSerializer
    
    def list(self, request, *args, **kwargs):
        # a = 1
        # return super().list(self, request, *args, **kwargs)
        """
        request.query_params
        <QueryDict: {'page': ['2']}>
        request.query_params.get("page", "1")
        """
        page_key = request.query_params.get("page", "1")
        key = settings.COLLECT_LIST.format(page=page_key)
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        paginated_response = self.get_paginated_response(data)
        cache.set(key, paginated_response.data, settings.CACHE_TTL)
        return paginated_response

    
    def retrieve(self, request, *args, **kwargs):
        collect_id = kwargs.get("pk")
        key = settings.COLLECT_DETAIL.format(collect_id=collect_id)
        cached = cache.get(key)
        if cached:
            return Response(cached)
        instance = self.get_object()
        data = self.get_serializer(instance).data
        cache.set(key, data, settings.CACHE_TTL)
        return Response(data)
        
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
