from django.urls import path
from .views import CreateUserAPIView, authenticate_user, UserGetUpdateAPIView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserAPIView.as_view()),
    path('obtain_token/', authenticate_user),
    path('update/', UserGetUpdateAPIView.as_view()),
]
