class ModificarPage {
  constructor() {
    this.tf = new TicketForm(Dom.id("form-ticket"));
    this.token = null;
  }

  iniciar() {
    Dom.id("b-curp").addEventListener("input", e => e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, ""));
    Dom.id("b-turno").addEventListener("input", e => e.target.value = e.target.value.replace(/\D/g, ""));
    Dom.id("form-buscar").addEventListener("submit", e => this.buscar(e));
    this.tf.form.addEventListener("submit", e => this.guardar(e));
  }

  async buscar(e) {
    e.preventDefault();
    const curp = Dom.id("b-curp").value.trim(), turno = Dom.id("b-turno").value.trim();
    const municipio_id = Dom.id("b-municipio").value;
    if (!TicketForm.CURP.test(curp)) { Notificador.mostrar("Escribe una CURP válida", "error"); return; }
    if (!turno) { Notificador.mostrar("Escribe tu número de turno", "error"); return; }

    if (!municipio_id) { Notificador.mostrar("Selecciona el municipio", "error"); return; }

    const r = await ApiClient.post("/api/v1/tickets/buscar", { curp, turno, municipio_id });
    if (!r.ok) { Notificador.mostrar(r.data?.error || "No encontrado", "error"); return; }

    this.token = r.data.token;
    this.tf.limpiar();
    this.tf.llenar(r.data.ticket);
    this.tf.bloquear(["curp", "municipio_id"]);
    Dom.id("turno").textContent = r.data.ticket.turno;
    Dom.id("resultado").hidden = true;
    Dom.id("edicion").hidden = false;
  }

  async guardar(e) {
    e.preventDefault();
    if (!this.tf.validar()) return;
    const r = await ApiClient.put(`/api/v1/tickets/publico/${this.token}`, this.tf.datos());
    if (r.status === 422) { this.tf.errores(r.data.errores); return; }
    if (!r.ok) { Notificador.mostrar(r.data?.error || "No se pudo guardar", "error"); return; }
    Dom.id("r-pdf").href = r.data.pdf_url;
    Dom.id("edicion").hidden = true;
    Dom.id("resultado").hidden = false;
    Notificador.mostrar("Solicitud actualizada");
  }
}

new ModificarPage().iniciar();
