from django import forms
from .models import Usuario

class NewsForm(forms.Form):
    theme = forms.CharField(label='Tema de las noticias', max_length=100)

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'contrasena']
