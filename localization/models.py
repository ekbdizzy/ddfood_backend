from django.db import models
from catalog.models import Product


class City(models.Model):
    name = models.CharField(max_length=100, default='', blank=True, verbose_name='Город:')
    query_id = models.CharField(max_length=100, default='', blank=True, verbose_name='Идентификатор:')
    address = models.CharField(max_length=500, blank=True, verbose_name='Адрес на главной странице сайта:')
    phone = models.CharField(max_length=40, blank=True, verbose_name='Телефон на главной странице сайта:')
    working_time = models.CharField(max_length=200, blank=True, verbose_name='Часы работы:')
    delivery_info = models.TextField(max_length=1000, verbose_name='Информация о доставке:')
    minimal_price_for_delivery = models.IntegerField(default=0, verbose_name='Минимальная сумма для доставки:')
    delivery_price = models.DecimalField(
        default=0, decimal_places=0, max_digits=5, verbose_name='Стоимость платной доставки:'
    )
    is_self_delivery = models.BooleanField(default=False, verbose_name='Есть самовывоз:')
    self_delivery_info = models.TextField(
        max_length=1000, verbose_name='Информация о самовывозе:', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        # ordering = ('-id',)
        verbose_name = 'Регион доставки'
        verbose_name_plural = 'Регионы доставки'


class ProductInStock(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город:')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт:', related_name='in_stock')
    is_available = models.BooleanField(default=False, verbose_name='В наличии')

    def __str__(self):
        return f'{self.product.name}: {self.city.name}'

    class Meta:
        # ordering = ('-id',)
        verbose_name = 'Наличие товара на складе'
        verbose_name_plural = 'Наличие товара на складе'

