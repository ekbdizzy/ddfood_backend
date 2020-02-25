from django.db import models

# Create your models here.


from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from user.user_manager import UserManager


# from coupon.models import Coupon


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    phone = models.CharField(unique=True, max_length=15, verbose_name='Телефон')
    first_name = models.CharField(max_length=100, blank=True, verbose_name='Имя, фамилия')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Пользователь активен")
    bonuses = models.IntegerField(default=0, verbose_name="Бонусы")
    is_staff = models.BooleanField(default=False, verbose_name="Персонал")
    is_superuser = models.BooleanField(default=False, verbose_name="Aдминистратор (полный доступ к управлению сайтом)")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('email', 'phone')

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ('email',)


class Partner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='partner')
    promo_code = models.CharField(blank=True, max_length=50)


class SalesManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    partners = models.ForeignKey(Partner, on_delete=models.PROTECT)


class InvitedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invited_user')
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, related_name='invited_user')
