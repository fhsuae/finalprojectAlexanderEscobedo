### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Final Project Nasa Explorer

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "space"  # Namespace for URLs of the 'space' app

# URL patterns specific to the 'space' app
urlpatterns = [
    # Homepage displaying NASA's Astronomy Picture of the Day (APOD)
    path('', views.homepage, name='homepage'),

    # EPIC Earth imagery gallery view
    path('epic-gallery/', views.EpicGalleryView.as_view(), name='epic_gallery'),

    # NASA Image Library search results view
    path('search-images/', views.NasaImageSearchView.as_view(), name='image_search'),

    # List and paginate exoplanet data from NASA archive
    path('exoplanets/', views.ExoplanetView.as_view(), name='exoplanets'),

    # Near-Earth asteroid data view
    path('asteroids/', views.AsteroidView.as_view(), name='asteroids'),

    # Display solar flare events from NASA DONKI API
    path('donki/', views.DONKIView.as_view(), name='donki'),

    # User login page using Django's built-in authentication views
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # User logout page with confirmation template
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),

    # User signup view to create a new account
    path('signup/', views.signup, name='signup'),

    # View to display logged-in user's favorite images
    path('favorites/', views.favorites, name='favorites'),

    # Endpoint to add an image to user's favorites (POST request expected)
    path('add-favorite/', views.add_favorite, name='add_favorite'),

    # Endpoint to remove a favorite image by its id
    path('remove-favorite/<int:fav_id>/', views.remove_favorite, name='remove_favorite'),

    # Endpoint to download a favorite image by its id
    path('download-favorite/<int:fav_id>/', views.download_favorite, name='download_favorite'),
]
