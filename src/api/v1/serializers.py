from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import serializers

from fees.models import Collect, Payment

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
        )


class PaymentCollectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collect
        fields = (
            "id",
            "name",
            "cause",
            "closing_to",
        )


class PaymentListModelSerializer(serializers.ModelSerializer):

    author = UserModelSerializer(
        many=False,
    )

    class Meta:
        model = Payment
        fields = (
            "id",
            "comment",
            "author",
            "collection",
            "amount",
            "created_at",
        )


class PaymentDetailModelSerializer(serializers.ModelSerializer):
    author = UserModelSerializer(
        many=False,
    )
    collection = PaymentCollectionModelSerializer(many=False)

    class Meta:
        model = Payment
        fields = (
            "id",
            "comment",
            "author",
            "collection",
            "amount",
            "created_at",
            "updated_at",
        )


class PaymentWriteModelSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Payment
        fields = (
            "comment",
            "amount",
            "author",
        )

    def to_representation(self, value):
        serializer = PaymentDetailModelSerializer(value)
        serializer.context["request"] = self.context["request"]
        return serializer.data


class CollectListModelSerializer(serializers.ModelSerializer):
    cause_display = serializers.CharField(source="get_cause_display", read_only=True)
    author = UserModelSerializer(
        many=False,
    )
    current_amount = serializers.SerializerMethodField(
        read_only=True,
    )
    current_amount_in_percent = serializers.SerializerMethodField(
        read_only=True,
    )

    class Meta:
        model = Collect
        fields = (
            "id",
            "name",
            "author",
            "cause",
            "cause_display",
            "current_amount",
            "current_amount_in_percent",
            "planned_amount",
            "image",
            "closing_to",
        )

    def get_current_amount(self, obj):
        """Количество человек сделавших пожертвования."""
        return Decimal(getattr(obj, "current_amount", "0.00"))

    def get_current_amount_in_percent(self, obj):
        """Количество человек сделавших пожертвования."""
        current_amount = getattr(obj, "current_amount", Decimal("0.00"))
        return round(current_amount / (obj.planned_amount / 100), 2)


class CollectDetailModelSerializer(serializers.ModelSerializer):
    author = UserModelSerializer(
        many=False,
    )
    count_supporters = serializers.SerializerMethodField(
        read_only=True,
    )
    current_amount = serializers.SerializerMethodField(
        read_only=True,
    )
    supporters_full_names = serializers.SerializerMethodField(
        read_only=True,
    )
    current_amount_in_percent = serializers.SerializerMethodField(
        read_only=True,
    )

    class Meta:
        model = Collect
        fields = (
            "id",
            "name",
            "author",
            "cause",
            "description",
            "planned_amount",
            "current_amount",
            "current_amount_in_percent",
            "supporters_full_names",
            "image",
            "closing_to",
            "count_supporters",
            "created_at",
            "updated_at",
        )

    def get_count_supporters(self, obj):
        """Количество человек сделавших пожертвования."""
        return getattr(obj, "count_supporters", 0)

    def get_current_amount(self, obj):
        """Количество человек сделавших пожертвования."""
        return Decimal(getattr(obj, "current_amount", "0.00"))

    def get_supporters_full_names(self, obj):
        """Количество человек сделавших пожертвования."""
        return getattr(obj, "supporters_full_names", [])

    def get_current_amount_in_percent(self, obj):
        """Количество человек сделавших пожертвования."""
        current_amount = getattr(obj, "current_amount", Decimal("0.00"))
        return round(current_amount / (obj.planned_amount / 100), 2)


class CollectWriteModelSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Collect
        fields = (
            "name",
            "description",
            "cause",
            "planned_amount",
            "closing_to",
            "image",
            "author",
        )

    def to_representation(self, value):
        serializer = CollectDetailModelSerializer(value)
        serializer.context["request"] = self.context["request"]
        return serializer.data
