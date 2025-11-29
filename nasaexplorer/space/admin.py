from django.contrib import admin
from .models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "image_title", "image_id", "created_at")
    search_fields = ("image_title", "image_id", "user__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
