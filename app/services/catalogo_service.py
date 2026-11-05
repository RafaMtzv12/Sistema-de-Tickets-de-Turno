from ..models import Asunto, Municipio, Nivel


class CatalogoService:
    @staticmethod
    def todos():
        return dict(
            municipios=Municipio.query.order_by(Municipio.nombre).all(),
            niveles=Nivel.query.order_by(Nivel.id).all(),
            asuntos=Asunto.query.order_by(Asunto.nombre).all(),
        )
