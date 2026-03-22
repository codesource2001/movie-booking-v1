from django.db import models
from movie.models import Movie
from theatre.models import Screen


class Show(models.Model):
    SHOW_STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='shows')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField()
    status = models.CharField(max_length=20, choices=SHOW_STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_time']
        unique_together = ['screen', 'start_time']

    def __str__(self):
        return f"{self.movie.title} - {self.screen.name} - {self.start_time}"
