from rest_framework import serializers
from .models import Product, Category, TradeMark


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'is_active')


class TradeMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeMark
        fields = ('name', )


class ProductSerializer(serializers.ModelSerializer):
    trade_mark = TradeMarkSerializer()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'article',
            'categories',
            'trade_mark',
            'mass',
            'measure',
            'contain',
            'protein',
            'fat',
            'carbs',
            'fibers',
            'energy_value_calories',
            'bread_ones',
            'krahmal',
            'dry_milk',
            'kletchatka',
            'isolat',
            'gluten',
            'inulin',
            'dukan_phase',
            'base_image',
            'best_before',
            'price',
            'sale',
            'promo',
        )

        # extra_kwargs = {'password': {'write_only': True},
        #                 'email': {'required': False},
        #                 'phone': {'required': False},
        #                 }



