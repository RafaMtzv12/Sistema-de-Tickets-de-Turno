from functools import wraps

from flask import redirect, request, session, url_for


class ApiError(Exception):
    def __init__(self, mensaje, status=400, errores=None):
        super().__init__(mensaje)
        self.mensaje, self.status, self.errores = mensaje, status, errores


class Seguridad:
    """Decoradores de control de acceso."""

    @staticmethod
    def login_requerido(f):
        """Protege páginas de la parte privada."""
        @wraps(f)
        def wrapper(*a, **k):
            if not session.get("admin_id"):
                return redirect(url_for("auth.login", next=request.path))
            return f(*a, **k)
        return wrapper

    @staticmethod
    def api_admin(f):
        """Protege endpoints de la API solo para administradores."""
        @wraps(f)
        def wrapper(*a, **k):
            if not session.get("admin_id"):
                raise ApiError("No autorizado", 401)
            return f(*a, **k)
        return wrapper
