from django.utils.deprecation import MiddlewareMixin

class DisableCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response

from django.shortcuts import redirect
from django.urls import reverse

class LogoutRequiredMiddleware:
    """
    Middleware para evitar que los usuarios accedan a páginas protegidas
    después de cerrar sesión al usar el botón 'atrás' del navegador.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path.startswith('/dashboard/'):
            return redirect(reverse('login'))  # Redirige al login si no está autenticado
        return self.get_response(request)
