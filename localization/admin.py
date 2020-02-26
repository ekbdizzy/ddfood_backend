from django.contrib import admin
from .models import City, ProductInStock


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    class Meta:
        model = City


@admin.register(ProductInStock)
class ProductInStockAdmin(admin.ModelAdmin):
    class Meta:
        model: ProductInStock

    list_display = ['product', 'city', 'is_available']
    list_filter = ['city__name', 'is_available']
