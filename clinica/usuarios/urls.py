from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView  # Agregar LogoutView aquí
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from .views import CustomLoginView, login_redirect, registro_paciente, dashboard_paciente, dashboard_doctor, dashboard_administrador, redirigir_dashboard, registrar_cita, crear_usuario

urlpatterns = [
    # Página principal
    path('', views.home, name='home'),
    
    # Autenticación
    path('login/', CustomLoginView.as_view(), name='login'),  # Usa solo tu CustomLoginView
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Logout redirige a la home
    path('login-redirect/', login_redirect, name='login_redirect'),

    # Registro
    path('registro/', registro_paciente, name='registro'),

    # Dashboards según el tipo de usuario
    path('dashboard/paciente/<int:paciente_id>/', views.dashboard_paciente, name='dashboard_paciente'),
    path('dashboard/doctor/', dashboard_doctor, name='dashboard_doctor'),
    path('dashboard/administrador/', dashboard_administrador, name='dashboard_administrador'),
    path('dashboard/', redirigir_dashboard, name='redirigir_dashboard'),

    # Funcionalidades adicionales
    path('registrar-cita/', registrar_cita, name='registrar_cita'),
    path('crear-usuario/', crear_usuario, name='crear_usuario'),
    
    #urls para citas en el dashboard_doctor
    path('programar-cita/<int:cita_id>/', views.programar_cita, name='programar_cita'),
    path('detalle-cita/<int:cita_id>/', views.detalle_cita, name='detalle_cita'),
    path('rechazar_cita/<int:cita_id>/', views.rechazar_cita, name='rechazar_cita'),
    # URLs para el doctor
    path('dashboard/doctor/detalles-cita/<int:cita_id>/', views.detalles_cita_doctor, name='detalles_cita_doctor'),
    path('editar-cita-doctor/<int:cita_id>/', views.editar_cita_doctor, name='editar_cita_doctor'),
    path('editar-cita-paciente/<int:cita_id>/', views.editar_cita_paciente, name='editar_cita_paciente'),
    
    path('dashboard/administrador/', views.listar_usuarios, name='dashboard_administrador'),
    path('usuario/<int:user_id>/', views.ver_detalles_usuario, name='ver_detalles_usuario'),
    path('usuarios/usuario/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/usuario/eliminar/<int:pk>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    
     path('citas/pendientes/', views.citas_pendientes, name='citas_pendientes'),
    path('citas/programadas/', views.citas_programadas, name='citas_programadas'),
    path('citas/rechazadas/', views.citas_rechazadas, name='citas_rechazadas'),


]