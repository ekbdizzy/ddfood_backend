from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class PromoCode(models.Model):
    code = models.CharField(max_length=50, verbose_name='Промокод')
    valid_from = models.DateField(verbose_name="Действителен с")
    valid_to = models.DateField(verbose_name="Действителен до")
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Процент скидки"
    )
    active = models.BooleanField(default=True, verbose_name="Aктивен")

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        ordering = ('-code',)
