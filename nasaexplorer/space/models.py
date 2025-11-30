### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Final Project Nasa Explorer

from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    """
    Model representing a user's favorite NASA image.
    Links a user to saved image data.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    image_id = models.CharField(max_length=500)  # Unique image identifier from NASA API
    image_title = models.CharField(max_length=255)  # Title or description of the image
    image_url = models.URLField(blank=True)  # URL to the image
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when favorited

    def __str__(self):
        return f"{self.user.username} - {self.image_title}"
