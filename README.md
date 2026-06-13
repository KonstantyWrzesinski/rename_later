Weather App

Project Overview

Weather App is a web application developed using Django that allows users to search for weather information for cities around the world. The application integrates with an external weather API to provide current weather conditions and a 3-day forecast.

Users can create accounts, log in, save their favorite cities, and quickly access weather information from a personalized dashboard.

⸻

Main Features

User Authentication

* User registration
* User login and logout
* Session-based authentication

Weather Search

* Search weather by city name
* Display current weather conditions
* Display temperature, humidity, wind speed, and weather description
* Weather condition icons

3-Day Forecast

* Forecast for the next three days
* Daily weather icons
* Maximum and minimum temperatures

User Dashboard

* Save favorite cities
* Display saved cities as interactive cards
* View weather information for saved cities
* Remove saved cities
* Personalized data stored per user account

User Interface

* Responsive design
* Dark/Light theme toggle
* Modern dashboard layout
* Animated home page sections
* Fixed navigation bar

⸻

Technologies Used

Backend

* Python
* Django

Frontend

* HTML
* CSS
* JavaScript

Database

* SQLite

External Services

* Weather API
* Geocoding API for city suggestions

⸻

Installation

1. Clone the repository

git clone <repository-url>
cd weather-app

2. Create a virtual environment

python -m venv venv

Activate it:

Windows:

venv\Scripts\activate

macOS/Linux:

source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Apply migrations

python manage.py migrate

5. Run the development server

python manage.py runserver

6. Open the application

http://127.0.0.1:8000

⸻

Project Structure

someapp
Contains:

* Home page
* Weather search functionality
* API integration
* Forecast generation

login_module

Contains:

* User authentication
* Registration and login forms
* Dashboard functionality
* Saved cities management

Templates

Contains all HTML templates used by the application.

Static Files

Contains CSS, JavaScript, icons, and other assets.

⸻

Authors:
Filip Cybowicz
Bartek Szucki
Konstanty Wrzesinski
Paweł Wilusz

This project was developed as part of a university software development project using the Kanban methodology.
