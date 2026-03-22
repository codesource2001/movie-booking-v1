from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'role']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'role']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Permissions', {'fields': ('role',)}),
        ('Additional Info', {'fields': ('phone', 'address', 'date_of_birth')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role & Permissions', {'fields': ('role',)}),
    )
