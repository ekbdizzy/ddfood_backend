from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls', namespace='user')),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('city/', include('localization.urls', namespace='city')),
    path('shop/', include('shop.urls', namespace='shop')),
]
