from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import user_logged_in
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

import jwt
from rest_framework_jwt.serializers import jwt_payload_handler

from user.models import User
from .serializers import UserSerializer


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data

        if not request.data.get('email', ''):
            return Response({'error': 'Укажите электронную почту'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=request.data.get('email', '')):
            return Response({'error': 'Пользователь с такой почтой уже существует'},
                            status=status.HTTP_400_BAD_REQUEST)

        if len(request.data.get('phone', '')) < 15:
            return Response({'error': 'Введите номер телефона в формате +7 XXX-XXX-XXXX'},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(phone=request.data.get('phone', '')):
            return Response({'error': 'Пользователь с таким телефоном уже существует'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            new_user = serializer.create(data)
            user_serializer = UserSerializer(new_user)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response({'error': 'error'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    """ Based on ObtainJSONWebToken"""

    email = request.data.get('email', '')
    password = request.data.get('password', '')
    phone = request.data.get('phone', '')

    user = User.objects.filter(Q(email=email) | Q(phone=phone))
    if user:
        user = user[0]

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


class UserGetUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(
            instance=request.user,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        serializer.update(request.user, data)

        new_password = request.data.get('password', {})

        if new_password:
            request.user.set_password(new_password)
            request.user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
