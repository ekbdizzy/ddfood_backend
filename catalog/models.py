from django.db import models
from django.urls import reverse


class TradeMark(models.Model):
    name = models.CharField(blank=True, max_length=100)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Торговая марка'
        verbose_name_plural = 'Торговые марки'


class Category(models.Model):
    name = models.CharField(blank=True, max_length=100)
    slug = models.SlugField(blank=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('catalog:products_by_category', kwargs={'category_slug': self.slug})

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.name)


class Product(models.Model):

    def image_folder(self, filename):
        """ Return full path for uploaded image """
        filename = '.'.join([self.slug, filename.split('.')[-1]])
        return f'products/{self.slug}/{filename}'

    MEASURE_CHOICES = (
        ("гр.", "гр."),
        ("кг.", "кг."),
        ("мл", "мл"),
        ("л", "л"),
        ("шт.", "шт.")
    )

    DUCAN_PHASES = (
        ('C 1 этапа', 'C 1 этапа'),
        ('Cо 2 этапа', 'Cо 2 этапа'),
        ('C 3 этапа', 'C 3 этапа'),
        ('C 4 этапа', 'C 4 этапа'),
    )

    PROMO_CHOISES = (
        ('Акция', "Акция"),
        ('Распродажа', 'Распродажа'),
        ('Хит', 'Хит'),
        ('Новинка', 'Новинка')
    )

    name = models.CharField(max_length=250, blank=True, null=True, default=None, verbose_name='Название:')
    slug = models.SlugField(blank=True, max_length=250)
    article = models.BigIntegerField(blank=True, default=0, verbose_name='Артикул:')
    categories = models.ManyToManyField(Category, through='CategoryOfProduct', related_name='products_list')
    trade_mark = models.ForeignKey(TradeMark, on_delete=models.CASCADE,
                                   blank=True, null=True, default=None,
                                   verbose_name='Торговая марка:')

    mass = models.CharField(max_length=5, blank=True, default=None, null=True, verbose_name='Масса или объем:')
    measure = models.CharField(choices=MEASURE_CHOICES, max_length=50, default="Граммы", verbose_name='Мера измерения')
    contain = models.TextField(max_length=1000, blank=True, null=True, default=None, verbose_name='Состав:')
    protein = models.DecimalField(max_digits=3, decimal_places=1, blank=True, default=0, verbose_name='Белки:')
    fat = models.DecimalField(max_digits=3, decimal_places=1, blank=True, default=0, verbose_name='Жиры:')
    carbs = models.DecimalField(max_digits=3, decimal_places=1, default=0, blank=True, verbose_name='Углеводы:')
    fibers = models.DecimalField(max_digits=3, decimal_places=1, blank=True, default=0,
                                 verbose_name='Пищевые волокна:')
    energy_value_calories = models.DecimalField(max_digits=5, decimal_places=1, blank=True, default=0,
                                                verbose_name='Ккал на 100 гр.:')
    bread_ones = models.CharField(max_length=40, blank=True, default='', verbose_name='Хлебные единицы, гр.:')
    krahmal = models.CharField(max_length=40, blank=True, default='', verbose_name='Крахмал, гр.:')
    dry_milk = models.CharField(max_length=40, blank=True, default='', verbose_name='Сухое молоко, гр.:')
    kletchatka = models.CharField(max_length=40, blank=True, default='', verbose_name='Клетчатка, гр.:')
    isolat = models.CharField(max_length=40, blank=True, default='', verbose_name='Изолят, гр.:')
    gluten = models.CharField(max_length=40, blank=True, default='', verbose_name='Глютен, гр.:')
    inulin = models.CharField(max_length=40, blank=True, default='', verbose_name='Инулин, гр.:')
    dukan_phase = models.CharField(choices=DUCAN_PHASES, max_length=50, blank=True)
    base_image = models.ImageField(upload_to=image_folder, verbose_name="Основное фото: ", blank=True)
    best_before = models.TextField(max_length=500, blank=True, null=True, default=None,
                                   verbose_name='Условия хранения:')
    price = models.DecimalField(max_digits=8, decimal_places=0, default=0, verbose_name='Цена, руб.:')
    sale = models.IntegerField(default=0, verbose_name='Процент скидки:')
    promo = models.CharField(choices=PROMO_CHOISES, max_length=50, default='', blank=True, verbose_name='Промо:')

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'product_slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class CategoryOfProduct(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, default=None)

    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продукта'

    def __str__(self):
        return str(self.category.name)


class ImageOfProduct(models.Model):

    def image_folder(self, filename):
        """ Return full path for uploaded image """
        filename = '.'.join([self.product.slug, filename.split('.')[-1]])
        return f'products/{self.product.slug}/{filename}'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, default=None,
                                related_name='images')

    image = models.ImageField(upload_to=image_folder)

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'
