from decimal import Decimal

from django.contrib import admin
from django.db.models import Sum

from fees.models import Collect, Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    search_fields = ("comment", "amount", "author", "collection")
    list_display = (
        "comment",
        "amount",
        "author",
    )
    list_per_page = 10

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("author", "collection")


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "description",
        "author",
    )
    list_display = (
        "name",
        "author",
        "closing_to",
    )
    readonly_fields = ("get_current_amount",)
    list_per_page = 10

    def get_current_amount(self, obj):
        return obj.payments.aggregate(Sum("amount", default=Decimal("0.00"))).get("amount__sum")

    get_current_amount.short_description = "Собрано средств"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("payments").select_related("author")
