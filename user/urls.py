from django.urls import path
from .views import CreateUserAPIView, authenticate_user

# from rest_framework_jwt.views import ObtainJSONWebToken

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('obtain_token/', authenticate_user),
]
