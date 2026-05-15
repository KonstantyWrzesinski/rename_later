from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/weather/', views.dashboard_weather_api, name='dashboard_weather_api'),
]