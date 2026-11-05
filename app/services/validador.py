import re

from ..extensions import db
from ..models import Asunto, Municipio, Nivel


class TicketValidator:
    NOMBRE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:[ '\-][A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$")
    CURP = re.compile(r"^[A-Z]{4}\d{6}[HM][A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z0-9]\d$")
    MAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
    TEL = re.compile(r"^\d{10}$")

    @classmethod
    def validar(cls, d):
        e = {}
        txt = lambda k: str(d.get(k) or "").strip()

        nc = txt("nombre_completo")
        if len(nc.split()) < 2 or not cls.NOMBRE.match(nc):
            e["nombre_completo"] = "Escribe nombre y apellido(s), solo letras."
        if not cls.CURP.match(txt("curp").upper()):
            e["curp"] = "CURP inválida (18 caracteres, formato oficial)."
        for c in ("nombre", "paterno"):
            if not cls.NOMBRE.match(txt(c)):
                e[c] = "Obligatorio, solo letras."
        if txt("materno") and not cls.NOMBRE.match(txt("materno")):
            e["materno"] = "Solo letras."
        if txt("telefono") and not cls.TEL.match(txt("telefono")):
            e["telefono"] = "Deben ser 10 dígitos."
        if not cls.TEL.match(txt("celular")):
            e["celular"] = "Obligatorio, 10 dígitos."
        if not cls.MAIL.match(txt("correo")):
            e["correo"] = "Correo inválido."
        for campo, modelo in (("nivel_id", Nivel), ("municipio_id", Municipio), ("asunto_id", Asunto)):
            try:
                ok = db.session.get(modelo, int(d.get(campo))) is not None
            except (TypeError, ValueError):
                ok = False
            if not ok:
                e[campo] = "Selecciona una opción válida."
        return e
