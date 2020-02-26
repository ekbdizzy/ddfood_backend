from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    class Meta:
        model = Order

    list_display = [
        'id',
        'full_name',
        'email',
        # 'delivery'
        'status',
        'created',
        'updated'
    ]
    list_filter = ['status', 'created', 'updated']
    inlines = [OrderItemInLine]
