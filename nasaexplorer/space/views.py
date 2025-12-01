### INF601 - Advanced Programming in Python
### Alexander Escobedo
### Final Project Nasa Explorer

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Favorite
from .utils import get_apod, get_epic_images, search_nasa_images
from django.core.paginator import Paginator


def homepage(request):
    """
    Render homepage with Astronomy Picture of the Day (APOD) data.
    If the NASA API call fails, an error message is displayed instead.
    """
    apod_data = get_apod()  # Fetch APOD data using helper function
    context = {"apod": apod_data}

    if apod_data is None:
        # Pass error message to template if API fails
        context["api_error"] = "NASA APOD data is currently unavailable. Please try again later."

    return render(request, "home.html", context)


def signup(request):
    """
    Handle user registration using Django's built-in UserCreationForm.
    If registration is successful, log the user in automatically and redirect to homepage.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # Bind form to POST data
        if form.is_valid():
            user = form.save()  # Create new user
            login(request, user)  # Log in newly created user
            return redirect("space:homepage")
    else:
        form = UserCreationForm()  # Empty form for GET request

    return render(request, "registration/signup.html", {"form": form})


@login_required
def favorites(request):
    """
    Display all favorite images saved by the currently logged-in user.
    Only accessible by authenticated users.
    """
    favs = Favorite.objects.filter(user=request.user)  # Query favorites for current user
    return render(request, "space/favorites.html", {"favorites": favs})


@login_required
def add_favorite(request):
    """
    Add a NASA image to the logged-in user's favorites.
    Prevent duplicate favorites by checking if the entry already exists.
    """
    if request.method == "POST":
        image_id = request.POST.get("image_id")
        image_title = request.POST.get("image_title")
        image_url = request.POST.get("image_url")

        if image_id and image_url:
            # get_or_create prevents duplicates by checking existence before insertion
            Favorite.objects.get_or_create(
                user=request.user,
                image_id=image_id,
                defaults={"image_title": image_title, "image_url": image_url},
            )
    # Redirect back to referring page or homepage if referrer missing
    return redirect(request.META.get("HTTP_REFERER", "space:homepage"))


@login_required
def remove_favorite(request, fav_id):
    """
    Remove a favorite image identified by its ID for the logged-in user.
    Ensures users can only delete their own favorites.
    """
    Favorite.objects.filter(id=fav_id, user=request.user).delete()
    return redirect(request.META.get("HTTP_REFERER", "space:favorites"))


class DONKIView(View):
    """
    Display recent solar flare events fetched from NASA's DONKI Space Weather API.
    """

    def get(self, request):
        from .utils import get_donki_events

        events = get_donki_events()
        context = {"events": events}

        if not events:
            # Show error if API call failed or returned no data
            context["api_error"] = "NASA DONKI data is currently unavailable. Please try again later."

        return render(request, "space/donki.html", context)


class AsteroidView(View):
    """
    Display near-Earth asteroid data for the current day using NASA NeoWs API.
    """

    def get(self, request):
        from .utils import get_asteroids

        asteroids = get_asteroids()
        context = {"asteroids": asteroids}

        if not asteroids:
            context["api_error"] = "NASA asteroid data is currently unavailable. Please try again later."

        return render(request, "space/asteroids.html", context)


class EpicGalleryView(View):
    """
    Display NASA EPIC Earth images gallery.
    Shows latest natural color images of Earth from EPIC satellite.
    """

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
    """
    Handle user search queries against NASA's Image and Video Library API.
    Results are paginated to improve load times and usability.
    Shows error message if no results found or API unavailable.
    """

    def get(self, request):
        query = request.GET.get("q", "")
        results = search_nasa_images(query) if query else []

        paginator = Paginator(results, 20)  # Paginate 20 results per page
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
    """
    Display a paginated list of NASA exoplanet data from the Exoplanet Archive.
    """

    def get(self, request):
        from .utils import get_exoplanets

        planets = get_exoplanets()
        paginator = Paginator(planets, 20)  # Show 20 exoplanets per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "page_obj": page_obj,
        }

        if not planets:
            context["api_error"] = "NASA exoplanet data is currently unavailable. Please try again later."

        return render(request, "space/exoplanets.html", context)
