from rest_framework import serializers
from .models import PromoCode


class PromoCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoCode
        fields = ('code',
                  # 'valid_from',
                  # 'valid_to',
                  'discount',
                  # 'is_active'
                  )
