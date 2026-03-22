from django.db import models
from user.models import User


class Theatre(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='theatres', null=True, blank=True)
    location = models.CharField(max_length=300)
    address = models.TextField()
    total_seats = models.IntegerField()
    seats_layout = models.JSONField(default=dict, help_text="JSON format for seat layout")
    facilities = models.JSONField(default=list, help_text="List of facilities like Parking, Food Court, etc.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Screen(models.Model):
    SCREEN_TYPE_CHOICES = [
        ('standard', 'Standard'),
        ('3d', '3D'),
        ('imax', 'IMAX'),
        ('4dx', '4DX'),
    ]

    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE, related_name='screens')
    name = models.CharField(max_length=100, help_text="Screen name like Screen 1, Screen 2, etc.")
    screen_type = models.CharField(max_length=20, choices=SCREEN_TYPE_CHOICES, default='standard')
    total_seats = models.IntegerField()
    seats_layout = models.JSONField(default=dict)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.theatre.name} - {self.name}"
