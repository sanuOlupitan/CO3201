from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    # Defining choices for the 'type' field
    CONTENT_TYPE = [
        ('Movie', 'Movie'),
        ('TV Show', 'TV Show'),
    ]
    # Metadata from the CSV
    show_id = models.CharField(max_length=20, unique=True)

    # Type field to distinguish Movies from TV Shows
    type = models.CharField(max_length=10, choices=CONTENT_TYPE, default='Movie')
    title = models.CharField(max_length=225)
    director = models.TextField(null=True, blank=True)
    cast = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=225, null=True, blank=True)
    release_year = models.IntegerField()
    rating = models.CharField(max_length=50, null=True, blank=True)
    duration = models.CharField(max_length=50, null=True, blank=True)
    listed_in = models.TextField() #Genres
    description = models.TextField()

    #The ML soup
    content_soup = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.type})"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        #Ensures a user can't add the same movie to their watchlist twice
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username}'s Watchlist: {self.movie.title}"





