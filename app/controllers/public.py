from flask import abort, render_template, send_file

from ..services.catalogo_service import CatalogoService
from ..services.pdf_service import PdfService
from ..services.token_service import TokenService
from .base import BaseController


class PublicController(BaseController):
    nombre = "public"

    def rutas(self):
        self.ruta("/", "solicitud", self.solicitud)
        self.ruta("/modificar", "modificar", self.modificar)
        self.ruta("/comprobante/<token>", "comprobante", self.comprobante)

    @staticmethod
    def respuesta_pdf(ticket):
        return send_file(PdfService().generar(ticket), mimetype="application/pdf",
                         download_name=f"turno-{ticket.turno}.pdf")

    def solicitud(self):
        return render_template("public/solicitud.html", **CatalogoService.todos())

    def modificar(self):
        return render_template("public/modificar.html", **CatalogoService.todos())

    def comprobante(self, token):
        ticket = TokenService.ticket(token)
        if not ticket:
            abort(404)
        return self.respuesta_pdf(ticket)
