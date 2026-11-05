class TurnoService:
    """Cada municipio lleva su propio contador: 1, 2, 3 ... n."""

    @staticmethod
    def siguiente(municipio):
        municipio.ultimo_turno += 1
        return municipio.ultimo_turno
