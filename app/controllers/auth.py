import io
import secrets

from captcha.image import ImageCaptcha
from flask import flash, redirect, render_template, request, send_file, session, url_for

from ..models import Usuario
from .base import BaseController


class CaptchaService:
    LETRAS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

    @classmethod
    def nuevo(cls):
        texto = "".join(secrets.choice(cls.LETRAS) for _ in range(5))
        session["captcha"] = texto
        buf = io.BytesIO()
        ImageCaptcha(width=180, height=60).write(texto, buf)
        buf.seek(0)
        return buf

    @staticmethod
    def validar(valor):
        esperado = session.pop("captcha", None)   # un captcha sirve para un solo intento
        return bool(esperado) and valor.strip().upper() == esperado


class AuthController(BaseController):
    nombre = "auth"

    def rutas(self):
        self.ruta("/captcha.png", "captcha", self.captcha)
        self.ruta("/login", "login", self.login, methods=["GET", "POST"])
        self.ruta("/logout", "logout", self.logout, methods=["POST"])

    def captcha(self):
        resp = send_file(CaptchaService.nuevo(), mimetype="image/png")
        resp.headers["Cache-Control"] = "no-store"
        return resp

    def login(self):
        if request.method == "POST":
            if not CaptchaService.validar(request.form.get("captcha", "")):
                flash("Captcha incorrecto.", "error")
            else:
                u = Usuario.query.filter_by(username=request.form.get("usuario", "").strip()).first()
                if u and u.check_password(request.form.get("password", "")):
                    session.clear()
                    session["admin_id"], session["admin_nombre"] = u.id, u.username
                    return redirect(self._destino_seguro(request.args.get("next", "")))
                flash("Usuario o contraseña incorrectos.", "error")
        return render_template("auth/login.html")

    def logout(self):
        session.clear()
        return redirect(url_for("auth.login"))

    @staticmethod
    def _destino_seguro(destino):
        if not destino.startswith("/") or destino.startswith("//"):
            return url_for("admin.dashboard")
        return destino
