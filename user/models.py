from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('admin', 'Admin'),
        ('theatre_owner', 'Theatre Owner'),
        ('staff', 'Staff'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_theatre_owner(self):
        return self.role == 'theatre_owner' or self.is_admin

    @property
    def is_staff_member(self):
        return self.role in ['staff', 'theatre_owner', 'admin'] or self.is_staff
