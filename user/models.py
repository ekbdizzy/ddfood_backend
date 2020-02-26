from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from user.user_manager import UserManager
from promo_code.models import PromoCode


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    phone = models.CharField(unique=True, max_length=15, verbose_name='Телефон')
    full_name = models.CharField(max_length=100, blank=True, verbose_name='Имя, фамилия')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Пользователь активен")
    bonuses = models.IntegerField(default=0, verbose_name="Бонусы")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    is_superuser = models.BooleanField(default=False, verbose_name="Aдминистратор (полный доступ к управлению сайтом)")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('phone',)

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ('email',)


class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='partner')
    promo_code = models.OneToOneField(PromoCode, on_delete=models.SET_NULL, related_name='partner', null=True)

    class Meta:
        verbose_name = 'Партнер'
        verbose_name_plural = 'Партнеры'

    def __str__(self):
        return str(f'{self.user.full_name}: {self.user.email}')


class SalesManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='sales_manager')
    partners = models.ForeignKey(Partner, on_delete=models.PROTECT, related_name='sales_manager')

    def __str__(self):
        return str(f'{self.user.full_name}: {self.user.email}')

    class Meta:
        verbose_name = 'Менеджер по продажам'
        verbose_name_plural = 'Менеджеры по продажам'


class InvitedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invited_user')
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, related_name='invited_user', null=True)

    class Meta:
        verbose_name = 'Привлеченный покупатель'
        verbose_name_plural = 'Привлеченные покупатели'

    def __str__(self):
        return str(f'{self.user.full_name}: {self.user.email}')
