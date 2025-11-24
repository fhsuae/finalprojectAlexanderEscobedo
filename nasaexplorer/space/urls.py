from django.urls import path
from . import views

app_name = "space"
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path("mars-gallery/", views.MarsGalleryView.as_view(), name="mars_gallery"),
    path("epic-gallery/", views.EpicGalleryView.as_view(), name="epic_gallery"),
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
]
