from django.shortcuts import render, HttpResponse
from.models import TodoItem

# Create your views here.
def home(request):
    return render(request, "home.html")

def todos(request):
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items})

def team(request):
    return render(request, "team.html")

def about(request):
    return render(request, "about.html")