from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario  # Asegúrate de importar tu modelo de usuario personalizado

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'is_staff')  # Ajusta los campos según tu modelo
    list_filter = ('is_staff', 'is_active', 'tipo_usuario')  # Agrega filtros según tus necesidades
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
        ('Tipo de usuario', {'fields': ('tipo_usuario',)}),  # Si tienes un campo personalizado
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'tipo_usuario', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)
