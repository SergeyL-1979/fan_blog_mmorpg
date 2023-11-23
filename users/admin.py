from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'activation_code')
    search_fields = ('username', 'email', 'activation_code')


admin.site.register(CustomUser, CustomUserAdmin)
