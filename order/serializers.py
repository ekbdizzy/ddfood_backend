from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'city',
            'created',
            'updated',
            'status',
            'promo_code',
            'discount',
            'total_price',
            'full_name',
            'phone',
            'email',
            'pay_method',
            'delivery',
            'address',
            'entrance',
            'floor',
            'apartment',
            'comments_from_client'
        )
