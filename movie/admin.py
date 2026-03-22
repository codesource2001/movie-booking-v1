from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'genre', 'duration', 'release_date', 'is_active']
    list_filter = ['genre', 'is_active', 'release_date']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    date_hierarchy = 'release_date'
    ordering = ['-release_date']
