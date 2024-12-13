from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Usuario(AbstractUser):
    ADMINISTRADOR = 'admin'
    DOCTOR = 'doctor'
    PACIENTE = 'paciente'
    
    TIPO_USUARIO_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (DOCTOR, 'Doctor'),
        (PACIENTE, 'Paciente'),
    ]

    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPO_USUARIO_CHOICES,
        default=PACIENTE
    )

    def __str__(self):
        return self.username


from django.utils.timezone import now

class Cita(models.Model):
    paciente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario': 'paciente'},
        related_name='citas_como_paciente'
    )
    doctor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario': 'doctor'},
        related_name='citas_como_doctor'
    )
    fecha = models.DateField(null=True, blank=True)  # Fecha programada
    hora = models.TimeField(null=True, blank=True)  # Hora programada
    motivo = models.TextField()
    estado = models.CharField(max_length=20, default='pendiente', choices=[
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada')
    ])
    creado_el = models.DateTimeField(default=now)
    creado_en = models.DateTimeField(default=now)  # Fecha y hora de creación

    def __str__(self):
        return f"Cita de {self.paciente.username} con {self.doctor.username} el {self.fecha} a las {self.hora} - {self.estado}"
    
    
    

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)  # Para saber si ya fue leída
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha y hora de creación

    def __str__(self):
        return f"Notificación para {self.user.username}: {self.message}"