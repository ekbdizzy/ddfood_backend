from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings

from catalog.models import Product, Category
from catalog.serializers import ProductSerializer, CategorySerializer
from localization.models import City
from localization.serializers import CitySerializer
from user.serializers import UserSerializer


class MainAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        city_id = request.data.get('city_id', '') or settings.DEFAULT_CITY_ID
        city = City.objects.get(query_id=city_id)
        categories = Category.objects.filter(is_active=True)
        products = Product.objects.all()

        city_serializer = CitySerializer(city)
        products_serializer = ProductSerializer(products, many=True)
        categories_serializer = CategorySerializer(categories, many=True)

        if request.user.is_authenticated:
            bonuses = request.user.bonuses
        else:
            bonuses = 0

        return Response({
            'city': city_serializer.data,
            'products': products_serializer.data,
            'categories': categories_serializer.data,
            'bonuses': bonuses
        }, status=status.HTTP_200_OK)
