from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Favorite
from .utils import get_apod, get_epic_images, search_nasa_images
from django.core.paginator import Paginator

def homepage(request):
    apod_data = get_apod()
    context = {"apod": apod_data}
    if apod_data is None:
        context["api_error"] = "NASA APOD data is currently unavailable. Please try again later."
    return render(request, "home.html", context)

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("space:homepage")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def favorites(request):
    favs = Favorite.objects.filter(user=request.user)
    return render(request, "space/favorites.html", {"favorites": favs})

@login_required
def add_favorite(request):
    if request.method == "POST":
        image_id = request.POST.get("image_id")
        image_title = request.POST.get("image_title")
        image_url = request.POST.get("image_url")
        if image_id and image_url is not None:
            # Prevent duplicates
            Favorite.objects.get_or_create(
                user=request.user,
                image_id=image_id,
                defaults={"image_title": image_title, "image_url": image_url},
            )
    return redirect(request.META.get("HTTP_REFERER", "space:homepage"))

@login_required
def remove_favorite(request, fav_id):
    Favorite.objects.filter(id=fav_id, user=request.user).delete()
    return redirect(request.META.get("HTTP_REFERER", "space:favorites"))


class DONKIView(View):
    def get(self, request):
        from .utils import get_donki_events
        events = get_donki_events()
        context = {"events": events}
        if not events:
            context["api_error"] = "NASA DONKI data is currently unavailable. Please try again later."
        return render(request, "space/donki.html", context)

class AsteroidView(View):
    def get(self, request):
        from .utils import get_asteroids
        asteroids = get_asteroids()
        context = {"asteroids": asteroids}
        if not asteroids:
            context["api_error"] = "NASA asteroid data is currently unavailable. Please try again later."
        return render(request, "space/asteroids.html", context)

class EpicGalleryView(View):
    def get(self, request):
        from .utils import get_epic_images
        images = get_epic_images()
        context = {
            "images": images,
            "overall_caption": "Latest EPIC Earth images from NASA.",
        }
        if not images:
            context["api_error"] = "NASA EPIC images are currently unavailable."
        return render(request, "space/epic_gallery.html", context)



class NasaImageSearchView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        results = search_nasa_images(query) if query else []
        paginator = Paginator(results, 20)  # 20 items per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "query": query,
            "page_obj": page_obj,
        }
        if query and not results:
            context["api_error"] = "No images found or NASA Image Library is currently unavailable."
        return render(request, "space/image_search.html", context)

class ExoplanetView(View):
    def get(self, request):
        from .utils import get_exoplanets
        planets = get_exoplanets()
        paginator = Paginator(planets, 20)  # 20 items per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            "page_obj": page_obj,
        }
        if not planets:
            context["api_error"] = "NASA exoplanet data is currently unavailable. Please try again later."
        return render(request, "space/exoplanets.html", context)