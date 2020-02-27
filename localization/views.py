from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import City
from .serializers import CitySerializer


class GetCityAPIView(APIView):
    permission_classes = (AllowAny,)
    default_city_id = settings.DEFAULT_CITY_ID

    def get(self, request, city_id):
        try:
            city = City.objects.get(query_id=city_id)

        except City.DoesNotExist:
            city = City.objects.get(query_id=settings.DEFAULT_CITY_ID)

        serializer = CitySerializer(city)
        return Response(serializer.data, status=status.HTTP_200_OK)
