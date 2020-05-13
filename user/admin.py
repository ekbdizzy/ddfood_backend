from django.contrib import admin
from .models import User, Partner, SalesManager, InvitedUser, PasswordRecovery


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    class Meta:
        model = Partner


@admin.register(SalesManager)
class SalesManagerAdmin(admin.ModelAdmin):
    class Meta:
        model = SalesManager


@admin.register(InvitedUser)
class InvitedUserAdmin(admin.ModelAdmin):
    class Meta:
        model = InvitedUser

    list_filter = ['partner', ]
    # list_display = ['user',]


@admin.register(PasswordRecovery)
class PasswordRecoveryAdmin(admin.ModelAdmin):
    class Meta:
        model = PasswordRecovery

    list_display = [
        'user',
        'link',
        'date_created',
        'is_active'
    ]

    list_filter = [
        'is_active',
        'date_created'
    ]

    search_fields = [
        'user'
    ]
