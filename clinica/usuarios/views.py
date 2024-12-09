from django.shortcuts import render, redirect
from .forms import RegistroPacienteForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404 
from .models import Cita
from django import forms
from .forms import CrearUsuarioForm
from django.urls import reverse_lazy
from datetime import datetime
from usuarios.models import Usuario  
from .forms import UsuarioForm 
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



    
def home(request):
    return render(request, 'usuarios/home.html')

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if user.tipo_usuario == 'paciente':
            return reverse_lazy('dashboard_paciente', kwargs={'paciente_id': user.id})
        elif user.tipo_usuario == 'doctor':
            return reverse_lazy('dashboard_doctor')
        elif user.tipo_usuario == 'admin':
            return reverse_lazy('dashboard_administrador')
        return reverse_lazy('home')  # Por si acaso

    
def login_redirect(request):
    # Lógica para redirigir a la página adecuada después del login
    if request.user.tipo_usuario == 'paciente':
        return redirect('dashboard_paciente')
    elif request.user.tipo_usuario == 'doctor':
        return redirect('dashboard_doctor')
    elif request.user.tipo_usuario == 'admin':
        return redirect('dashboard_administrador')
    else:
        return redirect('home')  # Si el usuario no tiene tipo definido
    
    
def registro_paciente(request):
    if request.method == 'POST':
        form = RegistroPacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige al login después de registrarse
    else:
        form = RegistroPacienteForm()
    return render(request, 'registro.html', {'form': form})


def get_success_url(self):
        # Llama a la función redirigir_dashboard para determinar adónde redirigir
        if self.request.user.tipo_usuario == 'paciente':
            return reverse_lazy('dashboard_paciente')
        elif self.request.user.tipo_usuario == 'doctor':
            return reverse_lazy('dashboard_doctor')
        elif self.request.user.tipo_usuario == 'admin':
            return reverse_lazy('dashboard_administrador')
        return reverse_lazy('home')  # Si no corresponde a ningún caso, redirige a home

@login_required
def dashboard_paciente(request, paciente_id):
    paciente = get_object_or_404(Usuario, id=paciente_id)
    citas = Cita.objects.filter(paciente=paciente).order_by('-fecha', '-hora')
    
    return render(request, 'usuarios/dashboard_paciente.html', {'citas': citas})

@login_required
def dashboard_doctor(request):
    if request.user.tipo_usuario != 'doctor':
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para acceder a esta página.'})
    
    return render(request, 'usuarios/dashboard_doctor.html')

@login_required
def citas_pendientes(request):
    citas_pendientes = Cita.objects.filter(doctor=request.user, estado='pendiente').order_by('-fecha', '-hora')
    return render(request, 'usuarios/citas_pendientes.html', {'citas_pendientes': citas_pendientes})

@login_required
def citas_programadas(request):
    citas_programadas = Cita.objects.filter(doctor=request.user, estado='aceptada').order_by('-fecha', '-hora')
    return render(request, 'usuarios/citas_programadas.html', {'citas_programadas': citas_programadas})

@login_required
def citas_rechazadas(request):
    citas_rechazadas = Cita.objects.filter(doctor=request.user, estado='rechazada').order_by('-fecha', '-hora')
    return render(request, 'usuarios/citas_rechazadas.html', {'citas_rechazadas': citas_rechazadas})



@login_required
def dashboard_administrador(request):
    if request.user.tipo_usuario != 'admin':
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para acceder a esta página.'})

    # Filtrar usuarios según su tipo
    administradores = Usuario.objects.filter(tipo_usuario='admin')
    doctores = Usuario.objects.filter(tipo_usuario='doctor')
    pacientes = Usuario.objects.filter(tipo_usuario='paciente')

    return render(request, 'usuarios/dashboard_administrador.html', {
        'administradores': administradores,
        'doctores': doctores,
        'pacientes': pacientes
    })


def redirigir_dashboard(request):
    if request.user.tipo_usuario == 'paciente':
        return redirect('dashboard_paciente')
    elif request.user.tipo_usuario == 'doctor':
        return redirect('dashboard_doctor')
    elif request.user.tipo_usuario == 'admin':
        return redirect('dashboard_administrador')
    return redirect('login')  # Por si acaso

@login_required
def registrar_cita(request):
    if request.method == 'POST':
        paciente = request.user  # El paciente que crea la cita
        doctor_id = request.POST.get('doctor')
        motivo = request.POST.get('motivo')

        doctor = get_object_or_404(Usuario, id=doctor_id)

        # Crear la cita con fecha y hora como None
        cita = Cita.objects.create(
            paciente=paciente,
            doctor=doctor,
            motivo=motivo,
            fecha=None,
            hora=None,
            estado='pendiente'
        )
        return redirect('dashboard_paciente', paciente_id=paciente.id)

    doctores = Usuario.objects.filter(tipo_usuario='doctor')
    return render(request, 'usuarios/registrar_cita.html', {'doctores': doctores})





class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['doctor', 'motivo']  # Eliminados 'fecha' y 'hora'

                
@login_required
def crear_usuario(request):
    if request.user.tipo_usuario != 'admin':
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para acceder a esta página.'})

    if request.method == 'POST':
        form = CrearUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_administrador')
    else:
        form = CrearUsuarioForm()

    return render(request, 'usuarios/crear_usuario.html', {'form': form})

#views para las citas en el dashboard doctor


def programar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        fecha_programada = request.POST.get('fecha')  # Recoge la fecha del formulario
        hora_programada = request.POST.get('hora')  # Recoge la hora del formulario
        
        # Guardamos la fecha y hora programada por el doctor
        cita.fecha = fecha_programada
        cita.hora = hora_programada
        cita.estado = 'aceptada'
        cita.save()

        return redirect('dashboard_doctor')
    
    return render(request, 'usuarios/programar_cita.html', {'cita': cita})


@login_required
def detalle_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    
    # Verificamos que el usuario sea el paciente asociado a la cita
    if request.user != cita.paciente:
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para ver los detalles de esta cita.'})
    
    # Enviamos solo la información necesaria al contexto
    return render(request, 'usuarios/detalle_cita.html', {
        'cita': cita
    })
    
@login_required
def detalles_cita_doctor(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.user.tipo_usuario != 'doctor' or cita.doctor != request.user:
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para ver esta cita.'})

    return render(request, 'usuarios/detalles_cita_doctor.html', {'cita': cita})



@login_required
def editar_cita_doctor(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    
    if request.user != cita.doctor:
        return redirect('dashboard_doctor')  # Redirigir si el doctor no es el asignado

    if request.method == 'POST':
        # Verificar que los valores no estén vacíos
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        if not fecha or not hora:
            return render(request, 'usuarios/editar_cita.html', {
                'cita': cita,
                'error': 'Todos los campos son obligatorios.',
            })

        # Actualizar los datos de la cita
        cita.fecha = fecha
        cita.hora = hora
        cita.save()

        return redirect('dashboard_doctor')

    return render(request, 'usuarios/editar_cita.html', {'cita': cita})


@login_required
def editar_cita_paciente(request, cita_id):
    # Obtener la cita y el paciente relacionado
    cita = get_object_or_404(Cita, id=cita_id)

    # Validar si la cita no está aceptada
    if cita.estado != 'aceptada':
        return render(request, 'error.html', {'mensaje': 'Solo puedes editar citas en estado "aceptada".'})

    paciente = cita.paciente  # Asegúrate de que esta relación exista en tu modelo
    doctores = Usuario.objects.filter(tipo_usuario='doctor')  # Lista de doctores disponibles

    if request.method == 'POST':
        # Obtener los datos enviados
        nuevo_doctor = get_object_or_404(Usuario, id=request.POST['doctor'])
        nuevo_motivo = request.POST['motivo']

        # Validación de campos vacíos
        if not nuevo_doctor or not nuevo_motivo:
            return render(request, 'usuarios/editar_cita_paciente.html', {
                'cita': cita,
                'doctores': doctores,
                'paciente': paciente,
                'error': "Por favor, completa todos los campos antes de continuar."
            })

        # Actualizamos la cita con el nuevo doctor y motivo
        cita.doctor = nuevo_doctor
        cita.motivo = nuevo_motivo
        cita.estado = 'pendiente'  # Cambiamos el estado a pendiente
        cita.fecha = None  # Reseteamos la fecha programada
        cita.hora = None  # Reseteamos la hora programada
        cita.save()

        # Redirigimos al dashboard del paciente después de actualizar la cita
        return redirect('dashboard_paciente', paciente_id=paciente.id)

    # Pasamos la cita, doctores y paciente al contexto
    return render(request, 'usuarios/editar_cita_paciente.html', {
        'cita': cita,
        'doctores': doctores,
        'paciente': paciente,
    })


@login_required
def rechazar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    
    if request.user.tipo_usuario != 'doctor':
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para realizar esta acción.'})

    # Cambiamos el estado a rechazado
    cita.estado = 'rechazada'
    cita.save()

    # Redirigimos al dashboard del doctor
    return redirect('dashboard_doctor')


@login_required
def listar_usuarios(request):
    if request.user.tipo_usuario != 'admin':
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para acceder a esta página.'})
    
    # Obtener usuarios separados por tipo
    pacientes = Usuario.objects.filter(tipo_usuario='paciente')
    doctores = Usuario.objects.filter(tipo_usuario='doctor')
    administradores = Usuario.objects.filter(tipo_usuario='admin')

    return render(request, 'usuarios/dashboard_administrador.html', {
        'pacientes': pacientes,
        'doctores': doctores,
        'administradores': administradores
    })


@login_required
def ver_detalles_usuario(request, user_id):
    if request.user.tipo_usuario != 'admin':
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para acceder a esta página.'})
    
    # Obtener el usuario por su ID
    usuario = get_object_or_404(Usuario, id=user_id)
    
    return render(request, 'usuarios/detalles_usuario.html', {'usuario': usuario})

@login_required
def editar_usuario(request, pk):
    if request.user.tipo_usuario != 'admin':
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para acceder a esta página.'})

    usuario = Usuario.objects.get(pk=pk)
    
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        username = request.POST.get('username')
        email = request.POST.get('email')
        tipo_usuario = request.POST.get('tipo_usuario')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Actualizamos el usuario
        usuario.username = username
        usuario.email = email
        usuario.tipo_usuario = tipo_usuario

        # Si la contraseña nueva está definida y es válida, la cambiamos
        if password:
            if password == password_confirm:
                usuario.set_password(password)  # Establecemos la nueva contraseña
                usuario.save()  # Guardamos el usuario
                update_session_auth_hash(request, usuario)  # Mantener la sesión activa
                return redirect('dashboard_administrador')  # Redirigimos al dashboard del admin
            else:
                # Si las contraseñas no coinciden, mostramos un error
                return render(request, 'usuarios/editar_usuario.html', {
                    'usuario': usuario,
                    'error': 'Las contraseñas no coinciden.'
                })
        
        # Si no hay cambio de contraseña, solo actualizamos los demás datos
        else:
            usuario.save()  # Guardamos los cambios sin cambiar la contraseña

        return redirect('dashboard_administrador')  # Redirigimos al dashboard de administrador

    else:
        return render(request, 'usuarios/editar_usuario.html', {'usuario': usuario})

@login_required
def eliminar_usuario(request, pk):
    if request.user.tipo_usuario != 'admin':
        return render(request, 'error.html', {'mensaje': 'No tienes permiso para acceder a esta página.'})
    
    usuario = get_object_or_404(Usuario, pk=pk)
    # Evitar que un administrador elimine su propia cuenta
    if request.user == usuario:
        messages.error(request, "No puedes eliminar tu propia cuenta.")
        return redirect('dashboard_administrador')
    
    usuario.delete()
    messages.success(request, f"El usuario '{usuario.username}' ha sido eliminado exitosamente.")
    return redirect('dashboard_administrador')











