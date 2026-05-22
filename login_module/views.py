from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm
from django.contrib.auth.decorators import login_required
from .forms import UserPreferenceForm
from .models import UserPreference
from django.http import JsonResponse
from someapp.services import get_current_weather, WeatherServiceError

# Create your views here.
# def login(request):
#     return render(request, "login.html")

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
    preference, created = UserPreference.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserPreferenceForm(instance=preference)

    return render(request, 'dashboard.html', {
        'form': form,
        'preference': preference
    })


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
    