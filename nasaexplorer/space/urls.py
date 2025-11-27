from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "space"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('epic-gallery/', views.EpicGalleryView.as_view(), name='epic_gallery'),
    path('search-images/', views.NasaImageSearchView.as_view(), name='image_search'),
    path('exoplanets/', views.ExoplanetView.as_view(), name='exoplanets'),
    path('asteroids/', views.AsteroidView.as_view(), name='asteroids'),
    path('donki/', views.DONKIView.as_view(), name='donki'),

    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),

    path('signup/', views.signup, name='signup'),

    path('favorites/', views.favorites, name='favorites'),
    path('add-favorite/', views.add_favorite, name='add_favorite'),
    path('remove-favorite/<int:fav_id>/', views.remove_favorite, name='remove_favorite'),

]
