from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
   #path('', include('django.contrib.auth.urls')),
   path('registration/',views.login, name = 'login'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('register/', views.sign_up, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
]