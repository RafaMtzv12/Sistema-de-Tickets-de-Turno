from flask import current_app
from itsdangerous import BadSignature, URLSafeSerializer

from ..extensions import db
from ..models import Ticket


class TokenService:
    """Token firmado para descargar/modificar un comprobante sin exponer el id."""

    @staticmethod
    def _s():
        return URLSafeSerializer(current_app.config["SECRET_KEY"], salt="ticket")

    @classmethod
    def generar(cls, ticket):
        return cls._s().dumps(ticket.id)

    @classmethod
    def ticket(cls, token):
        try:
            return db.session.get(Ticket, cls._s().loads(token))
        except BadSignature:
            return None
