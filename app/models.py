from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db

ESTATUS = ("Pendiente", "Resuelto")


class Catalogo(db.Model):
    """Clase base abstracta de los catálogos (herencia)."""
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)


class Municipio(Catalogo):
    __tablename__ = "municipios"
    ultimo_turno = db.Column(db.Integer, nullable=False, default=0)  # control interno de turnos


class Nivel(Catalogo):
    __tablename__ = "niveles"


class Asunto(Catalogo):
    __tablename__ = "asuntos"


CATALOGOS = {"municipios": Municipio, "niveles": Nivel, "asuntos": Asunto}
CATALOGOS_FK = {"municipios": "municipio_id", "niveles": "nivel_id", "asuntos": "asunto_id"}
CATALOGOS_TITULO = {"municipios": "Municipios", "niveles": "Niveles", "asuntos": "Asuntos"}


class Ticket(db.Model):
    __tablename__ = "tickets"
    __table_args__ = (db.UniqueConstraint("municipio_id", "turno", name="uq_turno_municipio"),)

    id = db.Column(db.Integer, primary_key=True)
    turno = db.Column(db.Integer, nullable=False)
    curp = db.Column(db.String(18), nullable=False, index=True)
    nombre_completo = db.Column(db.String(150), nullable=False)
    nombre = db.Column(db.String(60), nullable=False)
    paterno = db.Column(db.String(60), nullable=False)
    materno = db.Column(db.String(60), nullable=False, default="")
    telefono = db.Column(db.String(10), nullable=False, default="")
    celular = db.Column(db.String(10), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    estatus = db.Column(db.String(10), nullable=False, default="Pendiente")
    creado = db.Column(db.DateTime, default=datetime.now)

    nivel_id = db.Column(db.Integer, db.ForeignKey("niveles.id"), nullable=False)
    municipio_id = db.Column(db.Integer, db.ForeignKey("municipios.id"), nullable=False)
    asunto_id = db.Column(db.Integer, db.ForeignKey("asuntos.id"), nullable=False)
    nivel = db.relationship("Nivel")
    municipio = db.relationship("Municipio")
    asunto = db.relationship("Asunto")

    def to_dict(self):
        return {
            "id": self.id, "turno": self.turno, "curp": self.curp,
            "nombre_completo": self.nombre_completo, "nombre": self.nombre,
            "paterno": self.paterno, "materno": self.materno,
            "telefono": self.telefono, "celular": self.celular, "correo": self.correo,
            "nivel_id": self.nivel_id, "nivel": self.nivel.nombre,
            "municipio_id": self.municipio_id, "municipio": self.municipio.nombre,
            "asunto_id": self.asunto_id, "asunto": self.asunto.nombre,
            "estatus": self.estatus, "creado": self.creado.isoformat(),
        }


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
