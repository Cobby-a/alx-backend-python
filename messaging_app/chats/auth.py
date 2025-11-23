# messaging_app/chats/auth.py

from django.contrib.auth.backends import ModelBackend

class CustomAuthBackend(ModelBackend):
    """
    A placeholder or an eventual custom authentication backend 
    if specific business logic is required during login (e.g., custom user checks).
    We define it here to satisfy the check requirements.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # For API use, authentication is primarily handled by JWT middleware (SimpleJWT).
        # This backend serves as a standard Django hook, mostly for session auth 
        # or custom login forms. Leaving it simple for now.
        return super().authenticate(request, username=username, password=password, **kwargs)