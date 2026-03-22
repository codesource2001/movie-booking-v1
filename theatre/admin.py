from django.contrib import admin
from .models import Theatre, Screen


class ScreenInline(admin.TabularInline):
    model = Screen
    extra = 1
    fields = ['name', 'screen_type', 'total_seats']


@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'total_seats', 'is_active']
    list_filter = ['is_active', 'location']
    search_fields = ['name', 'address', 'location']
    list_editable = ['is_active']
    inlines = [ScreenInline]


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ['name', 'theatre', 'screen_type', 'total_seats']
    list_filter = ['screen_type', 'theatre']
    search_fields = ['name', 'theatre__name']
