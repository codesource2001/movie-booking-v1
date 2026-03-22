from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'booking', 'amount', 'method', 'status', 'transaction_id', 'payment_date']
    list_filter = ['status', 'method', 'payment_date']
    search_fields = ['booking__id', 'transaction_id', 'booking__user__username']
    date_hierarchy = 'payment_date'
    readonly_fields = ['transaction_id', 'payment_date', 'updated_at', 'payment_details']
    
    fieldsets = (
        ('Payment Info', {
            'fields': ('booking', 'amount', 'method')
        }),
        ('Transaction', {
            'fields': ('status', 'transaction_id', 'payment_details')
        }),
        ('Timestamps', {
            'fields': ('payment_date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
