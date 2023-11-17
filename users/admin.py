from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'phone_number', 'username', 'first_name', 'last_name', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные данные', {'fields': ('phone_number', 'address')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

