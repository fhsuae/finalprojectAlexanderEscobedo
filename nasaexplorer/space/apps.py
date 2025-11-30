### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Final Project Nasa Explorer

from django.apps import AppConfig


class SpaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'space'