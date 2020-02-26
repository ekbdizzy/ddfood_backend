from django.contrib import admin
from .models import Product, TradeMark, Category, CategoryOfProduct, ImageOfProduct
from localization.models import ProductInStock


class ProductCategoryInLine(admin.TabularInline):
    model = CategoryOfProduct
    extra = 1
    # raw_id_fields = ['product']


class ImagesInProductInLine(admin.StackedInline):
    model = ImageOfProduct
    extra = 1


class ProductInStockInLine(admin.StackedInline):
    model = ProductInStock
    extra = 1


@admin.register(TradeMark)
class ProducerAdmin(admin.ModelAdmin):
    class Meta:
        model = TradeMark
        ordering = ('name',)

    prepopulated_fields = {"slug": ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = Category

    prepopulated_fields = {"slug": ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'trade_mark', 'price')
    list_filter = ('trade_mark',)
    prepopulated_fields = {"slug": ('name',)}
    search_fields = ('name',)

    class Meta:
        model = Product
        ordering = ('name',)

    inlines = [ProductCategoryInLine, ImagesInProductInLine, ProductInStockInLine]

# class OrderItemInLine(admin.TabularInline):
#     model = OrderItem
#     raw_id_fields = ['product']
#     raw_id_fields = ['product']
