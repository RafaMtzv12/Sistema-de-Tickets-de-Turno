class SolicitudesPage {
  constructor() {
    this.tf = new TicketForm(Dom.id("form-ticket"));
    this.modal = Dom.id("modal");
    this.tbody = Dom.id("tbody");
    this.cache = [];
    this.editId = null;
    this.timer = null;
  }

  iniciar() {
    Dom.id("btn-nueva").addEventListener("click", () => this.abrir(null));
    Dom.id("btn-cancelar").addEventListener("click", () => this.modal.close());
    Dom.id("f-q").addEventListener("input", () => this.buscarConRetraso());
    Dom.id("f-estatus").addEventListener("change", () => this.cargar());
    Dom.id("f-mun").addEventListener("change", () => this.cargar());
    this.tbody.addEventListener("click", e => this.clickTabla(e));
    this.tbody.addEventListener("change", e => this.cambioEstatus(e));
    this.tf.form.addEventListener("submit", e => this.guardar(e));
    this.cargar();
  }

  buscarConRetraso() {
    clearTimeout(this.timer);
    this.timer = setTimeout(() => this.cargar(), 300);
  }

  async cargar() {
    const p = new URLSearchParams({
      q: Dom.id("f-q").value, estatus: Dom.id("f-estatus").value, municipio_id: Dom.id("f-mun").value,
    });
    const r = await ApiClient.get("/api/v1/tickets?" + p);
    this.cache = r.data || [];
    this.tbody.innerHTML = this.cache.map(t => this.fila(t)).join("");
    Dom.id("vacio").hidden = this.cache.length > 0;
  }

  fila(t) {
    return `
    <tr data-id="${t.id}">
      <td>${t.turno}</td>
      <td>${Dom.esc(t.municipio)}</td>
      <td>${Dom.esc(t.curp)}</td>
      <td>${Dom.esc([t.nombre, t.paterno, t.materno].join(" ").trim())}</td>
      <td>${Dom.esc(t.asunto)}</td>
      <td><select class="est ${t.estatus}" data-act="estatus">
        <option ${t.estatus === "Pendiente" ? "selected" : ""}>Pendiente</option>
        <option ${t.estatus === "Resuelto" ? "selected" : ""}>Resuelto</option>
      </select></td>
      <td class="acc">
        <a class="boton" href="/admin/comprobante/${t.id}" target="_blank">PDF</a>
        <button data-act="editar">Editar</button>
        <button data-act="borrar" class="peligro">Eliminar</button>
      </td>
    </tr>`;
  }

  abrir(t) {
    this.tf.limpiar();
    this.editId = t ? t.id : null;
    Dom.id("modal-titulo").textContent = t ? `Editar solicitud (turno ${t.turno})` : "Nueva solicitud";
    if (t) { this.tf.llenar(t); this.tf.bloquear(["municipio_id"]); }
    this.modal.showModal();
  }

  async clickTabla(e) {
    const b = e.target.closest("button[data-act]");
    if (!b) return;
    const id = +b.closest("tr").dataset.id;
    const t = this.cache.find(x => x.id === id);
    if (b.dataset.act === "editar") this.abrir(t);
    if (b.dataset.act === "borrar") await this.eliminar(t);
  }

  async eliminar(t) {
    if (!confirm(`¿Eliminar la solicitud del turno ${t.turno}?`)) return;
    const r = await ApiClient.delete(`/api/v1/tickets/${t.id}`);
    if (r.ok) { Notificador.mostrar("Solicitud eliminada"); this.cargar(); }
  }

  async cambioEstatus(e) {
    const s = e.target.closest("select[data-act='estatus']");
    if (!s) return;
    const id = +s.closest("tr").dataset.id;
    const r = await ApiClient.patch(`/api/v1/tickets/${id}/estatus`, { estatus: s.value });
    if (r.ok) { Notificador.mostrar("Estatus actualizado"); this.cargar(); }
    else Notificador.mostrar("No se pudo actualizar", "error");
  }

  async guardar(e) {
    e.preventDefault();
    if (!this.tf.validar()) return;
    const d = this.tf.datos();
    const r = this.editId
      ? await ApiClient.put(`/api/v1/tickets/${this.editId}`, d)
      : await ApiClient.post("/api/v1/tickets", d);
    if (r.status === 422) { this.tf.errores(r.data.errores); return; }
    if (!r.ok) { Notificador.mostrar(r.data?.error || "Error al guardar", "error"); return; }
    this.modal.close();
    Notificador.mostrar("Guardado correctamente");
    this.cargar();
  }
}

new SolicitudesPage().iniciar();
