from django.shortcuts import render, redirect
import serial
import time
from datetime import datetime, timedelta
from newsapi import NewsApiClient  # Asegúrate de que newsapi esté instalado
from .forms import NewsForm
import requests
from django.http import HttpResponse
from utils.facial_reco.facial_recognition import facialRecognition
from django.contrib.auth import login, authenticate
from .forms import UsuarioForm

# Create your views here.
def home(request):
    try:
        ser = serial.Serial('COM9', 9600)  
    except:
        print("No se pudo abrir el puerto serial")
    else:
        time.sleep(1)
        ser.write(b'1')
        print('portada')
        ser.close()
    finally:
        return render(request, 'core/index.html')

def login(request):
    return render(request, 'core/login.html')

def api(request):
    try:
        ser = serial.Serial('COM9', 9600)  
    except:
        print("No se pudo abrir el puerto serial")
    else:
        time.sleep(1)
        ser.write(b'2')  
        print('api')
        ser.close()
    finally:
        return render(request, 'core/api.html')

def inicio(request):
    try:
        ser = serial.Serial('COM9', 9600)  
    except:
        print("No se pudo abrir el puerto serial")
    else:
        time.sleep(1)
        ser.write(b'4') 
        print('inicio')
        ser.close()
    finally:
        return render(request, 'core/inicio.html')
    
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
            return render(request, 'core/noticias.html/', context)
    else:
        form = NewsForm()
    
    context = {'form': form}
    return render(request, 'core/noticias.html/', context)

def pregunta_ciudad(request):
    return render(request, 'core/pregunta_ciudad.html')

def obtener_clima(request):
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

            return render(request, 'core/clima.html', context)
        else:
            mensaje_error = f"No se pudieron obtener datos del tiempo para {ciudad}"
            return HttpResponse(mensaje_error, status=response.status_code)

    return render(request, 'core/pregunta_ciudad.html')


def registro_facial(request):
    if request.method == 'POST':
        usuario = request.POST.get('nombre')
        facialReco = facialRecognition("webpersonal/utils/facial_reco/DatasetFaces")
        if facialReco.recognize(user=usuario):
            return render(request, 'core/porcentaje.html', {'usuario': usuario})
        else:
            return render(request, 'core/error_registro.html', {'removedUser': facialReco.getRemovedUser()})


def inicio_sesion_facial(request):
    facialReco = facialRecognition("webpersonal/utils/facial_reco/DatasetFaces")
    #facialReco.train()
    facialReco.predict()
    prediction = facialReco.getPrediction()
    if prediction == "Desconocido":
        return render(request, 'core/error_inicio_facial.html')
    else:
        return render(request, 'core/confirmacion.html', {'usuario': prediction})
    

def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UsuarioForm()
    return render(request, 'core/login.html', {'form': form})


def iniciar_sesion(request):
    if request.method == 'POST':  
        email = request.POST.get('email')
        contrasena = request.POST.get('password')
        user = authenticate(request, email=email, password=contrasena)
        print(email, contrasena, user)
            
        if user is not None:
            login(request, user)
            print("Usuario autenticado. Redirigiendo a confirmacion.")

            # Aquí es donde quieres redirigir al usuario después del inicio de sesión
            #usuario = user.nombre
            return render(request, 'core/confirmacion.html', {'usuario': user.nombre})
        else:
            # El usuario no pudo iniciar sesión
            pass

    return render(request, 'core/error_inicio_facial.html')