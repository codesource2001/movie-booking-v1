from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'show', 'total_price', 'status', 'booking_date']
    list_filter = ['status', 'booking_date']
    search_fields = ['user__username', 'show__movie__title']
    date_hierarchy = 'booking_date'
    readonly_fields = ['booking_date', 'updated_at', 'seats', 'total_price']
    
    fieldsets = (
        ('Booking Info', {
            'fields': ('user', 'show', 'seats', 'total_price')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('booking_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
