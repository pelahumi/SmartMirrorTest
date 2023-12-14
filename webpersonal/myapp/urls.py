from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('confirmacion/', views.confirmacion, name="confirmacion"),
    path('api/', views.api, name="api"),
    path('api/ciudad/clima/', views.ciudad, name="ciudad"),
    path('api/ciudad/', views.clima, name="clima"),
    path('api/noticias/', views.noticias, name='noticias'),
]