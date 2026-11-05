class SolicitudPage {
  constructor() {
    this.tf = new TicketForm(Dom.id("form-ticket"));
  }

  iniciar() {
    this.tf.form.addEventListener("submit", e => this.enviar(e));
    Dom.id("btn-nuevo").addEventListener("click", () => this.nueva());
  }

  async enviar(e) {
    e.preventDefault();
    if (!this.tf.validar()) return;
    Dom.id("btn-generar").disabled = true;
    const r = await ApiClient.post("/api/v1/tickets", this.tf.datos());
    Dom.id("btn-generar").disabled = false;
    if (r.status === 422) { this.tf.errores(r.data.errores); return; }
    if (!r.ok) { Notificador.mostrar(r.data?.error || "No se pudo generar el turno", "error"); return; }
    this.mostrarResultado(r.data);
  }

  mostrarResultado(data) {
    const t = data.ticket;
    Dom.id("turno").textContent = t.turno;
    Dom.id("r-turno").textContent = t.turno;
    Dom.id("r-municipio").textContent = t.municipio;
    Dom.id("r-asunto").textContent = t.asunto;
    Dom.id("r-curp").textContent = t.curp;
    Dom.id("r-pdf").href = data.pdf_url;
    Dom.id("bloque-form").hidden = true;
    Dom.id("resultado").hidden = false;
  }

  nueva() {
    this.tf.limpiar();
    Dom.id("turno").textContent = "–";
    Dom.id("resultado").hidden = true;
    Dom.id("bloque-form").hidden = false;
  }
}

new SolicitudPage().iniciar();
