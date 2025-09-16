# from rest_framework.permissions import
from decimal import Decimal

from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.postgres.fields import ArrayField
from django.core.cache import cache
from django.db import transaction
from django.db.models import Count, OuterRef, Subquery, Sum, Value
from django.db.models.fields import CharField
from django.db.models.functions import Coalesce, Concat
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.v1.serializers import (
    CollectDetailModelSerializer,
    CollectListModelSerializer,
    CollectWriteModelSerializer,
    PaymentDetailModelSerializer,
    PaymentListModelSerializer,
    PaymentWriteModelSerializer,
)
from fees.models import Collect, Payment
from fees.tasks import send_email_task
from fees.utils import build_collect_email, build_payment_email


class PaymentModelViewSet(ModelViewSet):
    http_method_names = [
        "get",
        "post",
        "put",
        "delete",
    ]

    def get_queryset(self):
        collection = get_object_or_404(Collect, id=self.kwargs.get("collect_id"))
        return collection.payments.select_related("author", "collection").all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PaymentDetailModelSerializer
        elif self.action == "list":
            return PaymentListModelSerializer
        return PaymentWriteModelSerializer

    @swagger_auto_schema(operation_description="Список платежей")
    def list(self, request, *args, **kwargs):
        page_key = request.query_params.get("page", "1")
        collect_id = kwargs.get("collect_id")
        key = settings.PAYMENT_LIST.format(collect_id=collect_id, page=page_key)
        cached = cache.get(key)
        if cached is not None:
            return Response(cached)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        data = self.get_serializer(page, many=True).data
        paginated_response = self.get_paginated_response(data)
        cache.set(key, paginated_response.data, settings.CACHE_TTL)
        return paginated_response

    @swagger_auto_schema(operation_description="Подробный вывод о платеже")
    def retrieve(self, request, *args, **kwargs):
        collect_id = kwargs.get("collect_id")
        payment_id = kwargs.get("pk")
        key = settings.PAYMENT_DETAIL.format(
            collect_id=collect_id,
            payment_id=payment_id,
        )
        cached = cache.get(key)
        if cached:
            return Response(cached)
        instance = self.get_object()
        data = self.get_serializer(instance).data
        cache.set(key, data, settings.CACHE_TTL)
        return Response(data)

    @swagger_auto_schema(
        operation_description="Создание платежа",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Изменение платежа",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удаление платежа",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        collection = get_object_or_404(Collect, id=self.kwargs.get("collect_id"))
        instance = serializer.save(collection=collection)
        self._invalidate_full_cache(instance)
        self._send_payment_email(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._invalidate_full_cache(instance)

    def perform_destroy(self, instance):
        self._invalidate_full_cache(instance)
        instance.delete()

    @staticmethod
    def _invalidate_full_cache(payment: Payment) -> None:
        detail_key = settings.PAYMENT_DETAIL.format(
            collect_id=payment.collection.pk,
            payment_id=payment.pk,
        )
        list_key = settings.PAYMENT_LIST.format(collect_id=payment.collection.pk, page="*")
        cache.delete(detail_key)
        cache.delete_pattern(list_key)

    @staticmethod
    def _send_payment_email(payment: Payment) -> None:
        if payment.author.email is not None:
            subject, message, recipient_list, html_message = build_payment_email(
                author_name=payment.author.first_name,
                author_email=payment.author.email,
                amount=payment.amount,
                collect_name=payment.collection.name,
            )
            transaction.on_commit(
                lambda: send_email_task.delay(subject, message, recipient_list, html_message)
            )


class CollectModelViewSet(ModelViewSet):
    serializer_class = CollectDetailModelSerializer
    queryset = Collect.objects.select_related("author")
    http_method_names = [
        "get",
        "post",
        "put",
        "delete",
    ]

    def get_queryset(self):
        current_amount_subquery = Subquery(
            Payment.objects.filter(collection=OuterRef("pk"))
            .values("collection")
            .annotate(total=Sum("amount"))
            .values("total")
        )
        queryset = (
            super()
            .get_queryset()
            .annotate(current_amount=Coalesce(current_amount_subquery, Value(Decimal("0.00"))))
        )
        if self.action == "retrieve":
            count_subquery = Subquery(
                Payment.objects.filter(collection=OuterRef("pk"))
                .values("collection")
                .annotate(count=Count("author", distinct=True))
                .values("count")
            )

            names_subquery = Subquery(
                Payment.objects.filter(collection=OuterRef("pk"))
                .values("collection")
                .annotate(
                    full_names=ArrayAgg(
                        Concat(
                            "author__first_name",
                            Value(" "),
                            "author__last_name",
                            output_field=CharField(),
                        ),
                        distinct=True,
                    )
                )
                .values("full_names")
            )
            queryset = queryset.annotate(
                count_supporters=Coalesce(count_subquery, Value(0)),
                supporters_full_names=Coalesce(
                    names_subquery, Value([], output_field=ArrayField(CharField()))
                ),
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return CollectListModelSerializer
        if self.action == "retrieve":
            return CollectDetailModelSerializer
        return CollectWriteModelSerializer

    @swagger_auto_schema(operation_description="Список сборов")
    def list(self, request, *args, **kwargs):
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

    @swagger_auto_schema(operation_description="Подробный вывод о сборе")
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

    @swagger_auto_schema(
        operation_description="Создание сбора",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Изменение сбора",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удаление сбора",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save()
        self._invalidate_full_cache(instance)
        self._send_collection_email(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._invalidate_full_cache(instance)

    def perform_destroy(self, instance):
        self._invalidate_full_cache(instance)
        instance.delete()

    @staticmethod
    def _invalidate_full_cache(collection: Collect) -> None:
        detail_key = settings.COLLECT_DETAIL.format(collect_id=collection.pk)
        list_key = settings.COLLECT_LIST.format(page="*")
        cache.delete(detail_key)
        cache.delete_pattern(list_key)

    @staticmethod
    def _send_collection_email(collection: Collect) -> None:
        if collection.author.email is not None:
            subject, message, recipient_list, html_message = build_collect_email(
                author_name=collection.author.first_name,
                author_email=collection.author.email,
                planned_amount=collection.planned_amount,
                collect_name=collection.name,
            )
            transaction.on_commit(
                lambda: send_email_task.delay(subject, message, recipient_list, html_message)
            )
