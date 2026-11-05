from flask import abort, render_template

from ..extensions import db
from ..models import CATALOGOS, CATALOGOS_TITULO, Ticket
from ..services.catalogo_service import CatalogoService
from .base import BaseController
from .public import PublicController
from .seguridad import Seguridad


class AdminController(BaseController):
    nombre = "admin"
    prefijo = "/admin"

    def rutas(self):
        self.ruta("/dashboard", "dashboard", self.dashboard)
        self.ruta("/solicitudes", "solicitudes", self.solicitudes)
        self.ruta("/catalogos/<tipo>", "catalogo", self.catalogo)
        self.ruta("/comprobante/<int:tid>", "comprobante", self.comprobante)

    @Seguridad.login_requerido
    def dashboard(self):
        return render_template("admin/dashboard.html", **CatalogoService.todos())

    @Seguridad.login_requerido
    def solicitudes(self):
        return render_template("admin/solicitudes.html", **CatalogoService.todos())

    @Seguridad.login_requerido
    def catalogo(self, tipo):
        if tipo not in CATALOGOS:
            abort(404)
        return render_template("admin/catalogo.html", tipo=tipo, titulo=CATALOGOS_TITULO[tipo])

    @Seguridad.login_requerido
    def comprobante(self, tid):
        ticket = db.session.get(Ticket, tid) or abort(404)
        return PublicController.respuesta_pdf(ticket)
