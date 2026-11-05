from flask import Blueprint


class BaseController:
    """Clase base de los controladores (herencia y polimorfismo)."""
    nombre = None
    prefijo = None

    def __init__(self):
        self.bp = Blueprint(self.nombre, __name__, url_prefix=self.prefijo)
        self.rutas()

    def rutas(self):
        raise NotImplementedError("Cada controlador define sus rutas")

    def ruta(self, url, endpoint, vista, **opciones):
        self.bp.add_url_rule(url, endpoint=endpoint, view_func=vista, **opciones)

    def vista(self, url, endpoint, clase):
        self.bp.add_url_rule(url, view_func=clase.as_view(endpoint))
