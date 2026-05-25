from django.shortcuts import render

from .models import TodoItem
from .forms import CityForm
from .services import get_current_weather, WeatherServiceError
from django.core.cache import cache

def home(request):
    form = CityForm(request.POST or None)
    weather = None
    error = None

    popular_cities = cache.get("popular_cities")

    if popular_cities is None:
        popular_city_names = ["Warszawa", "Paris", "Barcelona", "Oslo"]
        popular_cities = []

        for city_name in popular_city_names:
            try:
                city_weather = get_current_weather(city_name)
                popular_cities.append(city_weather)
            except WeatherServiceError:
                pass

        cache.set("popular_cities", popular_cities, 300)  # Pobieranie Info z Api co 5 minut

    if request.method == "POST" and form.is_valid():
        city = form.cleaned_data["city"]

        try:
            weather = get_current_weather(city)
        except WeatherServiceError as exc:
            error = str(exc)

    return render(request, "home.html", {
        "form": form,
        "weather": weather,
        "error": error,
        "popular_cities": popular_cities,
    })


def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})


def team(request):
    return render(request, "team.html")


def about(request):
    return render(request, "about.html")