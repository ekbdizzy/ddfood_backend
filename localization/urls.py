from django.urls import path
from .views import GetCityAPIView

app_name = 'city'

urlpatterns = [
    path('<city_id>', GetCityAPIView.as_view(), name='get_city'),
]
