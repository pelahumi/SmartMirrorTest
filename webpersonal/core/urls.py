
from django.urls import path
from . import views
from .views import pregunta_ciudad, obtener_clima

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("registro/", views.registro, name="registro"),
    path("api/", views.api, name="api"),
    path('api/noticias/', views.noticias, name='noticias'),
    path('api/pregunta-ciudad/', pregunta_ciudad, name='pregunta_ciudad'),
    path('api/clima/', obtener_clima, name='obtener_clima'),
]

