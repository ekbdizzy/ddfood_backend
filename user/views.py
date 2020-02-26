from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import user_logged_in

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

import jwt
from rest_framework_jwt.serializers import jwt_payload_handler

from user.models import User
from .serializers import UserSerializer


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        new_user = serializer.create(data)
        user_serializer = UserSerializer(new_user)

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


# TODO ObtainJSONWebToken
@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    email = request.data.get('email', '')
    password = request.data.get('password', '')
    phone = request.data.get('phone', '')
    if email:
        user = get_object_or_404(User, email=email)
    else:
        user = get_object_or_404(User, phone=phone)

    if user and user.check_password(password):
        try:
            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, settings.SECRET_KEY)
            user_logged_in.send(sender=user.__class__, request=request, user=user)

            user_details = {
                'full_name': user.full_name,
                'email': user.email,
                'token': token
            }
            return Response(user_details, status=status.HTTP_200_OK)

        except Exception as exc:
            raise exc
    else:
        error = {'error': 'Неверный логин или пароль'}
        return Response(error, status=status.HTTP_403_FORBIDDEN)
