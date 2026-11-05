from flask import Flask, jsonify

from config import Config
from .extensions import db


class Aplicacion:
    """Application Factory orientada a objetos: construye y configura la app."""

    def __init__(self, config=Config):
        self.flask = Flask(__name__)
        self.config = config

    def construir(self):
        self.flask.config.from_object(self.config)
        db.init_app(self.flask)
        self._registrar_controladores()
        self._registrar_errores()
        self._inicializar_bd()
        return self.flask

    def _registrar_controladores(self):
        from .controllers.admin import AdminController
        from .controllers.api import ApiController
        from .controllers.auth import AuthController
        from .controllers.public import PublicController

        for controlador in (PublicController(), AuthController(), AdminController(), ApiController()):
            self.flask.register_blueprint(controlador.bp)

    def _registrar_errores(self):
        from .controllers.seguridad import ApiError
        self.flask.register_error_handler(ApiError, self.manejar_api_error)

    @staticmethod
    def manejar_api_error(e):
        return jsonify(error=e.mensaje, errores=e.errores), e.status

    def _inicializar_bd(self):
        from .services.seed import Seeder
        with self.flask.app_context():
            db.create_all()
            Seeder.sembrar()
