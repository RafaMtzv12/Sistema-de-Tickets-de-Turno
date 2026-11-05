from ..extensions import db
from ..models import Municipio, Ticket
from .turno_service import TurnoService


class TicketFactory:
    """Patrón de diseño FACTORY: centraliza la creación/normalización de tickets."""

    CAMPOS_TEXTO = ("nombre_completo", "nombre", "paterno", "materno", "telefono", "celular", "correo")

    @classmethod
    def _datos(cls, d):
        datos = {c: str(d.get(c) or "").strip() for c in cls.CAMPOS_TEXTO}
        datos["curp"] = str(d["curp"]).strip().upper()
        datos["correo"] = datos["correo"].lower()
        for c in ("nivel_id", "municipio_id", "asunto_id"):
            datos[c] = int(d[c])
        return datos

    @classmethod
    def crear(cls, d):
        datos = cls._datos(d)
        municipio = db.session.get(Municipio, datos["municipio_id"])
        return Ticket(turno=TurnoService.siguiente(municipio), estatus="Pendiente", **datos)

    @classmethod
    def actualizar(cls, ticket, d, cambiar_curp=False):
        datos = cls._datos(d)
        datos.pop("municipio_id")        # el turno pertenece al municipio: no se cambia
        if not cambiar_curp:
            datos.pop("curp")            # el público no puede cambiar su CURP
        for k, v in datos.items():
            setattr(ticket, k, v)
        return ticket
