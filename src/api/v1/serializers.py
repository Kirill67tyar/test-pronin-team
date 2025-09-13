from rest_framework import serializers

from django.contrib.auth import get_user_model
from fees.models import Collect, Payment
from decimal import Decimal

User = get_user_model()

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )
class PaymentModelSerializer(serializers.ModelSerializer):
    """
    action list:
        id
        name
        owner (nested или id/username)
        collection (id или brief info, как name коллекции)
        amount
        created_at
        
    action detail:
        Все из списка выше.
        updated_at
        Полный collection (nested serializer с деталями коллекции, если нужно).
    """
    class Meta:
        model = Payment
        fields = (
            'id',
            'name',
            'owner',
            'collection',
            'amount',
            'created_at',
            'updated_at',
        )


class CollectListModelSerializer(serializers.ModelSerializer):
    """
    action list:
        id (автоматически, как PK)
        name
        author (сериализованный как nested или просто username/id, в зависимости от нужд)
        cause (с readable label из choices, если используешь get_cause_display)
        planned_amount
        image (URL, если используешь ImageField)
        closing_to
        TODO current_amount_in_percent для этого нужно вычислять current_amount и вычислять по формуле
    """
    cause_display = serializers.CharField(source='get_cause_display', read_only=True)
    author = UserModelSerializer(
        many=False,
    )
    class Meta:
        model = Collect
        fields = (
            "id",
            "name",
            "author",
            "cause",
            "cause_display",
            "planned_amount",
            "image",
            "closing_to",
        )
        
    """
    action detail:
        Все из списка выше.
        description (полный текст).
        current_amount (вычисляемый: sum(Payment.amount for payment in self.payments.all()) via SerializerMethodField).
        count_supporters (вычисляемый: self.payments.values('owner').distinct().count()).
        Опционально: список связанных payments (nested serializer, но с pagination, если их много) или просто ссылки на них.
        Если нужно, добавь list_supported как method field, возвращающий список owners из payments.
    """
class CollectDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collect
        fields = (
            'id',
            'name',
            'author',
            'cause',
            'description',
            'planned_amount',
            'current_amount',
            'supporters_full_names',
            'image',
            'closing_to',
            'count_supporters',
        )
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
    
    def get_count_supporters(self, obj):
        """Количество человек сделавших пожертвования."""
        return getattr(obj, "count_supporters", 0)
    
    def get_current_amount(self, obj):
        """Количество человек сделавших пожертвования."""
        return getattr(obj, "current_amount", Decimal("0.00"))
    
    def get_supporters_full_names(self, obj):
        """Количество человек сделавших пожертвования."""
        return getattr(obj, "supporters_full_names", [])


class CollectWriteModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collect
        fields = (
            "name",
            "description",
            "cause",
            "planned_amount",
            "closing_to",
            "image",
        )
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


    def to_representation(self, value):
        serializer = CollectDetailModelSerializer(value)
        serializer.context['request'] = self.context['request']
        return serializer.data
