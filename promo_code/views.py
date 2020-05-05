from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import datetime

from .models import PromoCode
from .serializers import PromoCodeSerializer


class PromoCodeAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        code = request.data['code']
        promo_code = PromoCode.objects.filter(code=code,
                                              is_active=True,
                                              valid_from__lte=datetime.now(),
                                              valid_to__gte=datetime.now()
                                              )
        if promo_code:
            serializer = PromoCodeSerializer(promo_code[0])
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        return Response({'error': 'Промокод не действителен'}, status=status.HTTP_400_BAD_REQUEST)
