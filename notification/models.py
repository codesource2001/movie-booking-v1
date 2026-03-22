from django.db import models
from user.models import User


class Notification(models.Model):
    TYPE_CHOICES = [
        ('booking', 'Booking'),
        ('payment', 'Payment'),
        ('show', 'Show'),
        ('system', 'System'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    related_id = models.IntegerField(null=True, blank=True, help_text="Related object ID (booking_id, payment_id, etc.)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification {self.id} - {self.user.username} - {self.title}"
