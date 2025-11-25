from django.urls import path
from . import views

app_name = "space"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('epic-gallery/', views.EpicGalleryView.as_view(), name='epic_gallery'),
    path('search-images/', views.NasaImageSearchView.as_view(), name='image_search'),
    path("exoplanets/", views.ExoplanetView.as_view(), name="exoplanets"),
    path("asteroids/", views.AsteroidView.as_view(), name="asteroids"),
    path("donki/", views.DONKIView.as_view(), name="donki"),
]
