from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from localization.models import City
from promo_code.models import PromoCode
from catalog.models import Product
from user.models import User

PAY_METHODS = ([
    ('cash', 'Наличными курьеру'),
    ('card', 'Банковской картой курьеру при получении'),
    # ('online', 'Банковской картой онлайн')
])

DELIVERY_TYPES = [
    ('self', 'Самовывоз'),
    ('delivery', 'Доставка')
]

ORDER_STATUS = [
    ('Принят', 'Принят'),
    ('Подтвержден', 'Подтвержден'),
    ('Собран для самовывоза', 'Собран для самовывоза'),
    ('Передан на доставку', 'Передан на доставку'),
    ('Выполнен', 'Выполнен'),
    ('Не выполнен', 'Не выполнен'),
]


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Покупатель')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Регион доставки')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Получен')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменен статус')
    status = models.CharField(max_length=100,
                              default="Принят",
                              verbose_name='Статус заказа',
                              choices=ORDER_STATUS)

    promo_code = models.ForeignKey(PromoCode,
                                   on_delete=models.DO_NOTHING,
                                   null=True, blank=True,
                                   verbose_name='Промокод')

    discount = models.IntegerField(default=0,
                                   validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   verbose_name='Процент скидки')
    total_price = models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Cумма заказа')

    # customer_info
    full_name = models.CharField(max_length=100, default='', null=True, blank=True, verbose_name='Имя покупателя')
    phone = models.CharField(max_length=20, default='', null=True, blank=True, verbose_name='Телефон')
    email = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name='Email')
    pay_method = models.CharField(max_length=100,
                                  default='Наличными при получении',
                                  choices=PAY_METHODS,
                                  verbose_name='Способ оплаты')
    delivery = models.CharField(max_length=100,
                                default='delivery',
                                choices=DELIVERY_TYPES,
                                verbose_name='Доставка/самовывоз')

    # delivery
    address = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name='Адрес доставки')
    entrance = models.CharField(max_length=10, default='', null=True, blank=True, verbose_name='Подъезд')
    floor = models.CharField(max_length=10, default='', null=True, blank=True, verbose_name="Этаж")
    apartment = models.CharField(max_length=10, default='', null=True, blank=True, verbose_name="Квартира/Офис")

    comments_from_client = models.TextField(
        max_length=1000,
        default='',
        null=True,
        blank=True,
        verbose_name='Комментарии к заказу:'
    )
    comments_from_admin = models.TextField(max_length=1000,
                                           default='',
                                           null=True,
                                           blank=True,
                                           verbose_name='Комментарии от админстратора')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return "Заказ № {0}".format(str(self.id))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items', verbose_name='Продукт')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return str(self.id)
