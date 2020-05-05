from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls', namespace='user')),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('city/', include('localization.urls', namespace='city')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('promo_code/', include('promo_code.urls', namespace='promo_code')),
    path('order/', include('order.urls', namespace='orders'))
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)