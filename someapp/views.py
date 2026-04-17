from django.shortcuts import render
from .models import TodoItem
from .forms import CityForm
from .services import get_current_weather, WeatherServiceError


def home(request):
    form = CityForm(request.POST or None)
    weather = None
    error = None

    if request.method == "POST" and form.is_valid():
        city = form.cleaned_data["city"]
        try:
            weather = get_current_weather(city)
        except WeatherServiceError as exc:
            error = str(exc)

    return render(
        request,
        "home.html",
        {
            "form": form,
            "weather": weather,
            "error": error,
        },
    )


def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})


def team(request):
    return render(request, "team.html")


def about(request):
    return render(request, "about.html")