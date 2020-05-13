import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import PasswordRecovery, User
from .serializers import PasswordRecoverySerializer, UserSerializer


class CreatePasswordRecoveryLinkAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email', '')
        user = User.objects.filter(email=email)
        if not user:
            return Response({'error': 'Пользователь с такой почтой не существует'}, status=status.HTTP_400_BAD_REQUEST)

        active_links = PasswordRecovery.objects.filter(user__email=email)
        if active_links:
            for link in active_links:
                link.is_active = False
                link.save()

        PasswordRecovery.objects.create(
            user=user[0],
            link=str(uuid.uuid4()),
            is_active=True
        )

        # TODO send mail to user
        # http://localhost:8000/user/reset-password/?id=1&link=4e48767d-11e0-4dea-9d24-99c0036599c7

        return Response({'ok': 'Ссылка отправлена'}, status=status.HTTP_201_CREATED)

    def put(self, request):

        id = request.data.get('id', '')
        link = request.data.get('link', '')
        password = request.data.get('password', '')

        password_recovery = PasswordRecovery.objects.filter(user__id=id, link=link, is_active=True)

        if password_recovery:
            user = password_recovery[0].user
            user.set_password(password)
            user.save()

            password_recovery[0].is_active = False
            password_recovery[0].save()

            return Response({'ok': 'Пароль изменен'}, status=status.HTTP_200_OK)

        return Response({'error': 'Ссылка устарела, воспользуйтесь формой восстановления пароля.'}, status=status.HTTP_400_BAD_REQUEST)
