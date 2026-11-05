from sqlalchemy import func, or_

from ..extensions import db
from ..models import ESTATUS, Municipio, Ticket


class TicketRepository:
    @staticmethod
    def buscar(q="", estatus="", municipio_id=None):
        query = Ticket.query
        if q:
            like = f"%{q.strip()}%"
            completo = Ticket.nombre + " " + Ticket.paterno + " " + Ticket.materno
            query = query.filter(or_(Ticket.curp.ilike(like),
                                     Ticket.nombre_completo.ilike(like),
                                     completo.ilike(like)))
        if estatus in ESTATUS:
            query = query.filter(Ticket.estatus == estatus)
        if municipio_id:
            query = query.filter(Ticket.municipio_id == municipio_id)
        return query.order_by(Ticket.creado.desc()).all()

    @staticmethod
    def stats(municipio_id=None):
        q1 = db.session.query(Ticket.estatus, func.count(Ticket.id))
        q2 = (db.session.query(Municipio.nombre, Ticket.estatus, func.count(Ticket.id))
              .join(Ticket, Ticket.municipio_id == Municipio.id))
        if municipio_id:
            q1 = q1.filter(Ticket.municipio_id == municipio_id)
            q2 = q2.filter(Ticket.municipio_id == municipio_id)
        conteo = dict(q1.group_by(Ticket.estatus).all())
        por = {}
        for nombre, est, n in q2.group_by(Municipio.nombre, Ticket.estatus).all():
            por.setdefault(nombre, {"Pendiente": 0, "Resuelto": 0})[est] = n
        pend, res = conteo.get("Pendiente", 0), conteo.get("Resuelto", 0)
        return {"total": pend + res, "Pendiente": pend, "Resuelto": res,
                "por_municipio": [{"municipio": k, **v} for k, v in sorted(por.items())]}
