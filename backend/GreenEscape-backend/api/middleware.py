from django.shortcuts import redirect
from django.conf import settings

EXCLUDED_PATHS = ["/login/", "/register/", "/api/login/", "/api/register/"]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path not in EXCLUDED_PATHS:
            return redirect(settings.LOGIN_URL)  # Redirige vers LOGIN_URL
        return self.get_response(request)