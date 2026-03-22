from django.contrib import admin
from .models import Show


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ['movie', 'screen', 'start_time', 'price', 'available_seats', 'status']
    list_filter = ['status', 'screen__theatre', 'movie__genre']
    search_fields = ['movie__title', 'screen__name', 'screen__theatre__name']
    date_hierarchy = 'start_time'
    ordering = ['-start_time']
    readonly_fields = ['available_seats', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Show Info', {
            'fields': ('movie', 'screen', 'start_time', 'end_time', 'price')
        }),
        ('Status', {
            'fields': ('available_seats', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
