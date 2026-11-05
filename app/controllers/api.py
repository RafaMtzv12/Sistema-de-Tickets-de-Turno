from flask import jsonify, request, url_for
from flask.views import MethodView
from sqlalchemy import func

from ..extensions import db
from ..models import CATALOGOS, CATALOGOS_FK, ESTATUS, Ticket
from ..services.ticket_factory import TicketFactory
from ..services.ticket_repository import TicketRepository
from ..services.token_service import TokenService
from ..services.validador import TicketValidator
from .base import BaseController
from .seguridad import ApiError, Seguridad


class Peticion:
    """Utilidades para leer y validar las peticiones de la API."""

    @staticmethod
    def json():
        d = request.get_json(silent=True)
        if not isinstance(d, dict):
            raise ApiError("JSON inválido", 400)
        return d

    @staticmethod
    def ticket(tid):
        t = db.session.get(Ticket, tid)
        if not t:
            raise ApiError("Solicitud no encontrada", 404)
        return t

    @staticmethod
    def validar(d):
        errores = TicketValidator.validar(d)
        if errores:
            raise ApiError("Datos inválidos", 422, errores)

    @staticmethod
    def modelo_catalogo(tipo):
        if tipo not in CATALOGOS:
            raise ApiError("Catálogo no encontrado", 404)
        return CATALOGOS[tipo]

    @classmethod
    def nombre_catalogo(cls, modelo, excluir_id=None):
        nombre = str(cls.json().get("nombre") or "").strip()
        if not 2 <= len(nombre) <= 100:
            raise ApiError("El nombre debe tener entre 2 y 100 caracteres", 422)
        dup = modelo.query.filter(func.lower(modelo.nombre) == nombre.lower())
        if excluir_id:
            dup = dup.filter(modelo.id != excluir_id)
        if dup.first():
            raise ApiError("Ya existe un registro con ese nombre", 409)
        return nombre


# ---------- Público ----------
class CatalogosAPI(MethodView):
    def get(self):
        return jsonify({k: [{"id": o.id, "nombre": o.nombre} for o in m.query.order_by(m.nombre)]
                        for k, m in CATALOGOS.items()})


class BuscarAPI(MethodView):
    """Para modificar: el usuario se identifica con CURP + número de turno."""
    def post(self):
        d = Peticion.json()
        try:
            turno = int(d.get("turno"))
        except (TypeError, ValueError):
            raise ApiError("Turno inválido", 422)
        try:
            municipio_id = int(d.get("municipio_id"))
        except (TypeError, ValueError):
            raise ApiError("Municipio inválido", 422)
        t = Ticket.query.filter_by(curp=str(d.get("curp", "")).strip().upper(),
                                   turno=turno, municipio_id=municipio_id).first()
        if not t:
            raise ApiError("No se encontró una solicitud con esa CURP, turno y municipio", 404)
        return jsonify(ticket=t.to_dict(), token=TokenService.generar(t))


class PublicoAPI(MethodView):
    def put(self, token):
        t = TokenService.ticket(token)
        if not t:
            raise ApiError("Solicitud no encontrada", 404)
        d = Peticion.json()
        Peticion.validar(d)
        TicketFactory.actualizar(t, d, cambiar_curp=False)
        db.session.commit()
        return jsonify(ticket=t.to_dict(), pdf_url=url_for("public.comprobante", token=token))


# ---------- Tickets ----------
class TicketListAPI(MethodView):
    @Seguridad.api_admin
    def get(self):
        tickets = TicketRepository.buscar(request.args.get("q", ""), request.args.get("estatus", ""),
                                          request.args.get("municipio_id", type=int))
        return jsonify([t.to_dict() for t in tickets])

    def post(self):  # público: registrar solicitud
        d = Peticion.json()
        Peticion.validar(d)
        t = TicketFactory.crear(d)
        db.session.add(t)
        db.session.commit()
        return jsonify(ticket=t.to_dict(),
                       pdf_url=url_for("public.comprobante", token=TokenService.generar(t))), 201


class TicketAPI(MethodView):
    @Seguridad.api_admin
    def get(self, tid):
        return jsonify(Peticion.ticket(tid).to_dict())

    @Seguridad.api_admin
    def put(self, tid):
        t = Peticion.ticket(tid)
        d = Peticion.json()
        Peticion.validar(d)
        TicketFactory.actualizar(t, d, cambiar_curp=True)
        db.session.commit()
        return jsonify(t.to_dict())

    @Seguridad.api_admin
    def delete(self, tid):
        db.session.delete(Peticion.ticket(tid))
        db.session.commit()
        return "", 204


class EstatusAPI(MethodView):
    @Seguridad.api_admin
    def patch(self, tid):
        t = Peticion.ticket(tid)
        estatus = Peticion.json().get("estatus")
        if estatus not in ESTATUS:
            raise ApiError("Estatus inválido", 422)
        t.estatus = estatus
        db.session.commit()
        return jsonify(t.to_dict())


class StatsAPI(MethodView):
    @Seguridad.api_admin
    def get(self):
        return jsonify(TicketRepository.stats(request.args.get("municipio_id", type=int)))


# ---------- CRUD de catálogos (admin) ----------
class CatalogoAPI(MethodView):
    @Seguridad.api_admin
    def get(self, tipo):
        modelo, fk = Peticion.modelo_catalogo(tipo), CATALOGOS_FK[tipo]
        return jsonify([{"id": o.id, "nombre": o.nombre,
                         "en_uso": Ticket.query.filter(getattr(Ticket, fk) == o.id).count()}
                        for o in modelo.query.order_by(modelo.nombre)])

    @Seguridad.api_admin
    def post(self, tipo):
        modelo = Peticion.modelo_catalogo(tipo)
        o = modelo(nombre=Peticion.nombre_catalogo(modelo))
        db.session.add(o)
        db.session.commit()
        return jsonify(id=o.id, nombre=o.nombre), 201


class CatalogoItemAPI(MethodView):
    @staticmethod
    def _obtener(tipo, cid):
        o = db.session.get(Peticion.modelo_catalogo(tipo), cid)
        if not o:
            raise ApiError("Registro no encontrado", 404)
        return o

    @Seguridad.api_admin
    def put(self, tipo, cid):
        o = self._obtener(tipo, cid)
        o.nombre = Peticion.nombre_catalogo(type(o), excluir_id=cid)
        db.session.commit()
        return jsonify(id=o.id, nombre=o.nombre)

    @Seguridad.api_admin
    def delete(self, tipo, cid):
        o = self._obtener(tipo, cid)
        if Ticket.query.filter(getattr(Ticket, CATALOGOS_FK[tipo]) == cid).count():
            raise ApiError("No se puede eliminar: tiene solicitudes asociadas", 409)
        db.session.delete(o)
        db.session.commit()
        return "", 204


class ApiController(BaseController):
    nombre = "api"
    prefijo = "/api/v1"

    def rutas(self):
        self.vista("/catalogos", "catalogos", CatalogosAPI)
        self.vista("/tickets", "tickets", TicketListAPI)
        self.vista("/tickets/buscar", "buscar", BuscarAPI)
        self.vista("/tickets/publico/<token>", "publico", PublicoAPI)
        self.vista("/tickets/<int:tid>", "ticket", TicketAPI)
        self.vista("/tickets/<int:tid>/estatus", "estatus", EstatusAPI)
        self.vista("/stats", "stats", StatsAPI)
        self.vista("/admin/catalogos/<tipo>", "catalogo", CatalogoAPI)
        self.vista("/admin/catalogos/<tipo>/<int:cid>", "catalogo_item", CatalogoItemAPI)
