from django.urls import path
from .views import MainAPIView

app_name = 'shop'

urlpatterns = [
    path('', MainAPIView.as_view(), name='main')
]
