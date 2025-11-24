from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic, View

from .models import Choice, Question
from .utils import get_apod, get_mars_rover_photos, get_epic_images

def homepage(request):
    apod_data = get_apod()
    context = {
        "apod": apod_data,
    }
    return render(request, "home.html", context)

class MarsGalleryView(View):
    def get(self, request):
        rover = request.GET.get('rover', 'curiosity')
        earth_date = request.GET.get('earth_date')
        sol = request.GET.get('sol')

        # Convert sol to int if provided, else None
        if sol:
            try:
                sol = int(sol)
            except ValueError:
                sol = None

        photos = get_mars_rover_photos(rover, earth_date, sol)
        context = {
            'photos': photos,
            'rover': rover,
            'earth_date': earth_date,
            'sol': sol,
        }
        return render(request, 'space/mars_gallery.html', context)

class EpicGalleryView(View):
    def get(self, request):
        images = get_epic_images()
        context = {
            "images": images,
        }
        return render(request, "space/epic_gallery.html", context)

class IndexView(generic.ListView):
    template_name = "space/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "space/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "space/image_results.html"

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "space/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "space/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "space/image_results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "space/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("space:results", args=(question.id,)))
