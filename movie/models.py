from django.db import models


class Movie(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('sci_fi', 'Sci-Fi'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('animation', 'Animation'),
        ('documentary', 'Documentary'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    poster = models.ImageField(upload_to='movies/posters/', blank=True, null=True)
    trailer_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return self.title
