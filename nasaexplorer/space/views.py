from django.shortcuts import render
from django.views import View
from .utils import get_apod, get_epic_images, search_nasa_images


def homepage(request):
    apod_data = get_apod()
    context = {"apod": apod_data}
    return render(request, "home.html", context)

class DONKIView(View):
    def get(self, request):
        from .utils import get_donki_events
        events = get_donki_events()
        context = {"events": events}
        return render(request, "space/donki.html", context)


class AsteroidView(View):
    def get(self, request):
        from .utils import get_asteroids
        asteroids = get_asteroids()
        context = {"asteroids": asteroids}
        return render(request, "space/asteroids.html", context)


class EpicGalleryView(View):
    def get(self, request):
        images = get_epic_images()
        context = {"images": images}
        return render(request, "space/epic_gallery.html", context)

class NasaImageSearchView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        results = search_nasa_images(query) if query else []
        context = {"query": query, "results": results}
        return render(request, "space/image_search.html", context)

class ExoplanetView(View):
    def get(self, request):
        from .utils import get_exoplanets
        planets = get_exoplanets()
        context = {"planets": planets}
        return render(request, "space/exoplanets.html", context)

