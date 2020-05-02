from django.urls import path
from .views import PromoCodeAPIView

app_name = 'promo_code'

urlpatterns = [
    path(r'check/', PromoCodeAPIView.as_view()),

]
