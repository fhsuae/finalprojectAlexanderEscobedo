### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Final Project Nasa Explorer

from django.contrib import admin
from .models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """
    Admin configuration for Favorite model.
    Displays useful fields and enables search/filter.
    """
    list_display = ("user", "image_title", "image_id", "created_at")
    search_fields = ("image_title", "image_id", "user__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
