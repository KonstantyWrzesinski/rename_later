from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from django.views.decorators.csrf import csrf_exempt
from .models import SavedCity
from django.http import JsonResponse
from someapp.services import get_current_weather, WeatherServiceError


def sign_in(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')
        
        form = LoginForm()
        return render(request,'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('dashboard')
        
        # either form not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'users/login.html',{'form': form})

def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login') 

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', { 'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/register.html', {'form': form}) 

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def dashboard_weather_api(request):
    city = request.GET.get("city", "").strip()

    if not city:
        return JsonResponse(
            {
                "ok": False,
                "error": "Nie podano miasta.",
            },
            status=400,
        )

    try:
        weather = get_current_weather(city)
    except WeatherServiceError as exc:
        return JsonResponse(
            {
                "ok": False,
                "error": str(exc),
            },
            status=502,
        )

    return JsonResponse(
        {
            "ok": True,
            "weather": weather,
        }
    )

@login_required
@require_http_methods(["POST"])
def save_city(request):

    data = json.loads(request.body)
    city = data.get("city", "").strip()

    if not city:
        return JsonResponse({
            "ok": False,
            "error": "City is required"
        }, status=400)

    SavedCity.objects.get_or_create(
        user=request.user,
        city_name=city
    )

    return JsonResponse({
        "ok": True
    })

@login_required
@require_http_methods(["DELETE"])
def delete_city(request):

    data = json.loads(request.body)
    city = data.get("city", "").strip()

    SavedCity.objects.filter(
        user=request.user,
        city_name=city
    ).delete()

    return JsonResponse({
        "ok": True
    })

@login_required
def get_saved_cities(request):

    cities = SavedCity.objects.filter(
        user=request.user
    ).values_list("city_name", flat=True)

    return JsonResponse({
        "ok": True,
        "cities": list(cities)
    })