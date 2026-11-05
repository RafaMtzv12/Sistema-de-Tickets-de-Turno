class DashboardPage {
  constructor() {
    this.graficaEstatus = null;
    this.graficaMunicipios = null;
  }

  iniciar() {
    document.querySelectorAll("input[name='modo']")
      .forEach(r => r.addEventListener("change", () => this.cambiarModo()));
    Dom.id("filtro-mun").addEventListener("change", () => this.cargar());
    this.cargar();
  }

  modo() {
    return document.querySelector("input[name='modo']:checked").value;
  }

  cambiarModo() {
    Dom.id("filtro-mun").disabled = this.modo() === "total";
    this.cargar();
  }

  async cargar() {
    const select = Dom.id("filtro-mun");
    const porMunicipio = this.modo() === "municipio";
    const url = "/api/v1/stats" + (porMunicipio ? `?municipio_id=${select.value}` : "");
    const r = await ApiClient.get(url);
    const s = r.data;

    Dom.id("vista-actual").textContent = porMunicipio
      ? `Mostrando: ${select.options[select.selectedIndex].text}`
      : "Mostrando: total de solicitudes";
    Dom.id("k-total").textContent = s.total;
    Dom.id("k-pend").textContent = s.Pendiente;
    Dom.id("k-res").textContent = s.Resuelto;
    this.dibujarEstatus(s);
    this.dibujarMunicipios(s);
  }

  dibujarEstatus(s) {
    this.graficaEstatus?.destroy();
    this.graficaEstatus = new Chart(Dom.id("g-estatus"), {
      type: "doughnut",
      data: { labels: ["Pendiente", "Resuelto"],
              datasets: [{ data: [s.Pendiente, s.Resuelto], backgroundColor: ["#e6a23c", "#2e8b57"] }] },
      options: { responsive: true, maintainAspectRatio: false,
                 plugins: { title: { display: true, text: "Estatus de solicitudes" } } },
    });
  }

  dibujarMunicipios(s) {
    this.graficaMunicipios?.destroy();
    this.graficaMunicipios = new Chart(Dom.id("g-municipios"), {
      type: "bar",
      data: { labels: s.por_municipio.map(m => m.municipio),
              datasets: [
                { label: "Pendiente", data: s.por_municipio.map(m => m.Pendiente), backgroundColor: "#e6a23c" },
                { label: "Resuelto", data: s.por_municipio.map(m => m.Resuelto), backgroundColor: "#2e8b57" },
              ] },
      options: { responsive: true, maintainAspectRatio: false,
                 plugins: { title: { display: true, text: "Solicitudes por municipio" } },
                 scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true, ticks: { precision: 0 } } } },
    });
  }
}

new DashboardPage().iniciar();
