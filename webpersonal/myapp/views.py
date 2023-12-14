from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def confirmacion(request):
    return render(request, "confirmacion.html")   

def api(request):
    return render(request, "api.html")