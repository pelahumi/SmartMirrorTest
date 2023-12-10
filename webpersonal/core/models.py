from django.db import models

# Create your models here.

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    contrasena = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre