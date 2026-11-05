from ..extensions import db
from ..models import Asunto, Municipio, Nivel, Usuario


class Seeder:
    """Datos iniciales: administrador y catálogos de ejemplo."""

    @classmethod
    def sembrar(cls):
        cls._admin()
        cls._catalogo(Municipio, ("Municipio A", "Municipio B", "Municipio C"))
        cls._catalogo(Nivel, ("Preescolar", "Primaria", "Secundaria", "Media superior"))
        cls._catalogo(Asunto, ("Inscripción", "Cambio de escuela", "Constancia de estudios",
                               "Certificado", "Aclaración de datos", "Baja"))
        db.session.commit()

    @staticmethod
    def _admin():
        if not Usuario.query.first():
            u = Usuario(username="admin")
            u.set_password("admin123")
            db.session.add(u)

    @staticmethod
    def _catalogo(modelo, nombres):
        if not modelo.query.first():
            db.session.add_all([modelo(nombre=n) for n in nombres])
