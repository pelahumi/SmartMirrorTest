from django.shortcuts import render
from django.http import HttpResponse
import requests
from datetime import datetime, timedelta
from newsapi import NewsApiClient 
from .forms import NewsForm

# Create your views here.
def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def confirmacion(request):
    return render(request, "confirmacion.html")   

def api(request):
    return render(request, "api.html")

def ciudad(request):
    return render(request, "ciudad.html")

def clima(request):
    if request.method == 'POST':
        ciudad = request.POST.get('ciudad', '')
        api_key = "beca443305c5fcb28b732af45d0b0114"
        if not ciudad:
            mensaje_error = "Por favor, ingresa una ciudad."
            return HttpResponse(mensaje_error, status=400)

        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&lang=es"

        response = requests.get(url)
        clima_data = response.json()

        if response.status_code == 200:
            temperatura_celsius = clima_data['main']['temp'] - 273.15

            context = {
                'temperatura': f"{temperatura_celsius:.2f}°C",
                'condicion': clima_data['weather'][0]['description'],
                'humedad': f"{clima_data['main']['humidity']}%",
                'viento': f"{clima_data['wind']['speed']} m/s",
            }

            return render(request, 'clima.html', context)
        else:
            mensaje_error = f"No se pudieron obtener datos del tiempo para {ciudad}"
            return HttpResponse(mensaje_error, status=response.status_code)

    return render(request, 'ciudad.html')

def noticias(request):
    if request.method == 'POST':
        # Crea una instancia del formulario y rellena los campos con la información de la solicitud
        form = NewsForm(request.POST)
        
        # Valida el formulario
        if form.is_valid():
            # Obtiene el tema de las noticias
            theme = form.cleaned_data['theme']
            

            # Obtiene la fecha actual
            current_date = datetime.now()
            newsapi = NewsApiClient(api_key="9aaaf2a83e8b4c59a2fac9ae1dcf58a8")
            # Realiza la solicitud a la API
            data = newsapi.get_everything(q=theme, language='es', sort_by='relevancy', page_size=100)

            # Obtiene la lista de artículos
            articles = data['articles']

            # Filtra las noticias que tienen menos de dos días de antigüedad
            filtered_news = [article for article in articles if
                             (current_date - datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")) > timedelta(days=2)]

            context = {'filtered_news': filtered_news}
            return render(request, 'noticias.html/', context)
    else:
        form = NewsForm()
    
    context = {'form': form}
    return render(request, 'noticias.html/', context)