from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from .models import Cita
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class RegistroPacienteForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Introduce un correo válido.")

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = Usuario.PACIENTE  # Asignamos automáticamente el tipo "paciente"
        if commit:
            user.save()
        return user

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['doctor', 'motivo']
          

class CrearUsuarioForm(UserCreationForm):
    tipo_usuario = forms.ChoiceField(choices=Usuario.TIPO_USUARIO_CHOICES)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'tipo_usuario', 'password1', 'password2']


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'tipo_usuario']
        widgets = {
            'tipo_usuario': forms.Select(choices=Usuario.TIPO_USUARIO_CHOICES),
        }
        
        
class EditarPerfilPacienteForm(UserChangeForm):
    class Meta:
        model = Usuario  # Cambia 'User' por 'Usuario'
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if Usuario.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise ValidationError("Este nombre de usuario ya está en uso. Por favor, elige otro.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class PasswordResetForm(forms.Form):
    email_or_username = forms.CharField(max_length=255, label="Correo o Nombre de Usuario")
    new_password = forms.CharField(widget=forms.PasswordInput, label="Nueva Contraseña")    
    
    
    
    
    
    
    
    
    
    
    
    
    