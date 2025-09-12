from rest_framework import serializers

from django.contrib.auth import get_user_model
from fees.models import Collect, Payment

User = get_user_model()

class PaymentModelSerializer(serializers.ModelSerializer):
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

class CollectModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collect
        fields = (
            'id',
            'name',
            'author',
            'cause',
            'description',
            'planned_amount',
            'image',
            'closing_to',
        )

