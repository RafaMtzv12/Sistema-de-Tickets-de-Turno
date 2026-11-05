class CatalogoPage {
  constructor() {
    this.tipo = Dom.id("catalogo").dataset.tipo;
    this.base = `/api/v1/admin/catalogos/${this.tipo}`;
    this.lista = [];
  }

  iniciar() {
    Dom.id("form-nuevo").addEventListener("submit", e => this.agregar(e));
    Dom.id("tbody").addEventListener("click", e => this.clickTabla(e));
    this.cargar();
  }

  async cargar() {
    const r = await ApiClient.get(this.base);
    this.lista = r.data || [];
    Dom.id("tbody").innerHTML = this.lista.map(o => `
      <tr data-id="${o.id}">
        <td>${Dom.esc(o.nombre)}</td>
        <td>${o.en_uso}</td>
        <td class="acc">
          <button data-act="editar">Editar</button>
          <button data-act="borrar" class="peligro">Eliminar</button>
        </td>
      </tr>`).join("");
  }

  async agregar(e) {
    e.preventDefault();
    const r = await ApiClient.post(this.base, { nombre: Dom.id("nombre").value });
    if (r.ok) { Dom.id("nombre").value = ""; Notificador.mostrar("Registro agregado"); this.cargar(); }
    else Notificador.mostrar(r.data?.error || "Error", "error");
  }

  async clickTabla(e) {
    const b = e.target.closest("button[data-act]");
    if (!b) return;
    const id = +b.closest("tr").dataset.id;
    const o = this.lista.find(x => x.id === id);
    if (b.dataset.act === "editar") await this.editar(o);
    else await this.eliminar(o);
  }

  async editar(o) {
    const nuevo = prompt("Nuevo nombre:", o.nombre);
    if (nuevo === null) return;
    const r = await ApiClient.put(`${this.base}/${o.id}`, { nombre: nuevo });
    if (r.ok) { Notificador.mostrar("Registro actualizado"); this.cargar(); }
    else Notificador.mostrar(r.data?.error || "Error", "error");
  }

  async eliminar(o) {
    if (!confirm(`¿Eliminar "${o.nombre}"?`)) return;
    const r = await ApiClient.delete(`${this.base}/${o.id}`);
    if (r.ok) { Notificador.mostrar("Registro eliminado"); this.cargar(); }
    else Notificador.mostrar(r.data?.error || "Error", "error");
  }
}

new CatalogoPage().iniciar();
