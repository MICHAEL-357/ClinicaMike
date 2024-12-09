from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from .models import Cita


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