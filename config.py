import os

BASE = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "cambia-esta-clave-en-produccion")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE, "ticket_turno.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
