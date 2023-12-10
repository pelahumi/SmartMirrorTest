
from django.urls import path
from . import views
from .views import pregunta_ciudad, obtener_clima, registro

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login, name="login"),
    path("registro/", views.registro, name="registro"),
    path("confirmacion/", views.inicio_sesion_facial, name="confirmacion"),
    path("iniciar_sesion/", views.iniciar_sesion, name="iniciar_sesion"),
    path("face_registro/", views.registro_facial, name="face_registro"),
    path("face_registro/error_registro/", views.registro_facial, name="error_registro"),
    path("face_registro/error_inicio_facial/", views.inicio_sesion_facial, name="error_inicio_facial"),
    path("confirmacion/api/", views.api, name="api"),
    path('confirmacion/api/noticias/', views.noticias, name='noticias'),
    path('confirmacion/api/pregunta-ciudad/', pregunta_ciudad, name='pregunta_ciudad'),
    path('confirmacion/api/clima/', obtener_clima, name='obtener_clima'),
]

