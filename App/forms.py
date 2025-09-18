import django.forms as forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Avatar

class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        help_texts = {llave: '' for llave in fields}

class ActualizarPerfilForm(UserChangeForm):
    email = forms.EmailField( required=True, label="Email")
    first_name = forms.CharField(label="Nombre", max_length=30, required=True)
    last_name = forms.CharField(label="Apellido", max_length=30, required=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        help_texts = {llave: '' for llave in fields}

class AvatarForm(forms.ModelForm):    
    class Meta:
        model = Avatar
        fields = ['imagen']