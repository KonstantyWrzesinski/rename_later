from django.urls import path 
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("todos/", views.todos, name="Todos"),
    path("team/",views.team, name="Team"),
    path("about/",views.about, name="About")
]