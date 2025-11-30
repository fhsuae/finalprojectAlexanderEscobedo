### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Final Project Nasa Explorer

from django.contrib import admin
from django.urls import include, path
from space import views as space_views

# Root URL configuration for the entire Django project
urlpatterns = [
    # Root URL redirects to the space app's homepage view
    path("", space_views.homepage, name="home"),

    # Include all URLs defined in the 'space' app under /space/
    path("space/", include("space.urls")),

    # Admin interface URLs
    path("admin/", admin.site.urls),
]
