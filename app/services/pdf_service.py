import io

import qrcode
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


class SingletonMeta(type):
    """Patrón de diseño SINGLETON: una sola instancia por clase."""
    _instancias = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            cls._instancias[cls] = super().__call__(*args, **kwargs)
        return cls._instancias[cls]


class PdfService(metaclass=SingletonMeta):
    AZUL = (0.18, 0.44, 0.75)

    def generar(self, t):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter)
        W, H = letter

        c.setFillColorRGB(*self.AZUL)
        c.rect(0, H - 3 * cm, W, 3 * cm, stroke=0, fill=1)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(2 * cm, H - 1.8 * cm, "Ticket de Turno")
        c.setFont("Helvetica", 11)
        c.drawString(2 * cm, H - 2.5 * cm, "Comprobante de solicitud")
        c.circle(W - 3 * cm, H - 1.5 * cm, 1 * cm, stroke=0, fill=1)
        c.setFillColorRGB(*self.AZUL)
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(W - 3 * cm, H - 1.5 * cm - 7, str(t.turno))

        c.setFillColorRGB(0, 0, 0)
        y = H - 4.5 * cm
        filas = [
            ("Turno", str(t.turno)),
            ("Municipio", t.municipio.nombre),
            ("Fecha de registro", t.creado.strftime("%d/%m/%Y %H:%M")),
            ("Estatus", t.estatus),
            ("CURP", t.curp),
            ("Alumno", f"{t.nombre} {t.paterno} {t.materno}".strip()),
            ("Quien realiza el trámite", t.nombre_completo),
            ("Teléfono", t.telefono or "-"),
            ("Celular", t.celular),
            ("Correo", t.correo),
            ("Nivel", t.nivel.nombre),
            ("Asunto", t.asunto.nombre),
        ]
        for etiqueta, valor in filas:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(2 * cm, y, etiqueta + ":")
            c.setFont("Helvetica", 11)
            c.drawString(7 * cm, y, valor)
            y -= 0.8 * cm

        # QR con la CURP del alumno
        qbuf = io.BytesIO()
        qrcode.make(t.curp).save(qbuf, format="PNG")
        qbuf.seek(0)
        c.drawImage(ImageReader(qbuf), W - 7 * cm, 3.5 * cm, 5 * cm, 5 * cm)
        c.setFont("Helvetica", 9)
        c.drawCentredString(W - 4.5 * cm, 3 * cm, "QR: CURP del alumno")

        # Código de barras (municipio + turno)
        codigo = f"{t.municipio_id:02d}{t.turno:05d}"
        code128.Code128(codigo, barHeight=1.5 * cm).drawOn(c, 2 * cm, 4.5 * cm)
        c.drawString(2 * cm, 4 * cm, codigo)

        c.setFont("Helvetica-Oblique", 9)
        c.drawString(2 * cm, 1.5 * cm, "Presenta este comprobante el día de tu atención.")
        c.showPage()
        c.save()
        buf.seek(0)
        return buf
