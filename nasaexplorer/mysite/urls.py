from django.contrib import admin
from django.urls import include, path
from space import views as space_views

urlpatterns = [
    path("", space_views.homepage, name="home"),
    path("space/", include("space.urls")),
    path("admin/", admin.site.urls),
]
