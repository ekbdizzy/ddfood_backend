from rest_framework import serializers
from .models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = (
            'name',
            'query_id',
            'address',
            'phone',
            'working_time',
            'delivery_info',
            'minimal_price_for_delivery',
            'delivery_price',
            'is_self_delivery',
            'self_delivery_info',
        )
