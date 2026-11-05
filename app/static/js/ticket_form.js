class TicketForm {
  static NOMBRE = /^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:[ '\-][A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$/;
  static CURP = /^[A-Z]{4}\d{6}[HM][A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z0-9]\d$/;
  static MAIL = /^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$/;

  constructor(form) {
    this.form = form;
    this.reglas = {
      nombre_completo: v => (v.trim().split(/\s+/).length >= 2 && TicketForm.NOMBRE.test(v.trim())) ? "" : "Escribe nombre y apellido(s), solo letras.",
      curp: v => TicketForm.CURP.test(v.trim().toUpperCase()) ? "" : "CURP inválida (18 caracteres, formato oficial).",
      nombre: v => TicketForm.NOMBRE.test(v.trim()) ? "" : "Obligatorio, solo letras.",
      paterno: v => TicketForm.NOMBRE.test(v.trim()) ? "" : "Obligatorio, solo letras.",
      materno: v => (!v.trim() || TicketForm.NOMBRE.test(v.trim())) ? "" : "Solo letras.",
      telefono: v => (!v || /^\d{10}$/.test(v)) ? "" : "Deben ser 10 dígitos.",
      celular: v => /^\d{10}$/.test(v) ? "" : "Obligatorio, 10 dígitos.",
      correo: v => TicketForm.MAIL.test(v.trim()) ? "" : "Correo inválido.",
      nivel_id: v => v ? "" : "Selecciona un nivel.",
      municipio_id: v => v ? "" : "Selecciona un municipio.",
      asunto_id: v => v ? "" : "Selecciona un asunto.",
    };
    this.nombres = Object.keys(this.reglas);
    this._enlazar();
  }

  campo(n) { return this.form.elements[n]; }

  _enlazar() {
    ["telefono", "celular"].forEach(n =>
      this.campo(n).addEventListener("input", e => e.target.value = e.target.value.replace(/\D/g, "").slice(0, 10)));
    this.campo("curp").addEventListener("input",
      e => e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, ""));
    this.nombres.forEach(n => {
      const el = this.campo(n);
      el.addEventListener("blur", () => this.validarCampo(n));
      el.addEventListener("change", () => this.validarCampo(n));
      el.addEventListener("input", () => {
        if (el.closest(".campo").classList.contains("invalido")) this.validarCampo(n);
      });
    });
  }

  marcar(n, msg) {
    const el = this.campo(n);
    const c = el.closest(".campo");
    c.querySelector(".error").textContent = msg;
    c.classList.toggle("invalido", !!msg);
    c.classList.toggle("valido", !msg && el.value !== "");
  }

  validarCampo(n) {
    const msg = this.reglas[n](this.campo(n).value);
    this.marcar(n, msg);
    return !msg;
  }

  validar() {
    const r = this.nombres.map(n => this.validarCampo(n));
    this.form.querySelector(".invalido input, .invalido select")?.focus();
    return !r.includes(false);
  }

  datos() {
    const d = {};
    this.nombres.forEach(n => d[n] = this.campo(n).value);
    d.curp = d.curp.toUpperCase();
    return d;
  }

  llenar(t) {
    this.nombres.forEach(n => this.campo(n).value = t[n] ?? "");
  }

  errores(obj) {
    Object.entries(obj || {}).forEach(([k, m]) => { if (this.campo(k)) this.marcar(k, m); });
  }

  bloquear(nombres) {
    nombres.forEach(n => {
      const el = this.campo(n);
      if (el.tagName === "SELECT") el.disabled = true; else el.readOnly = true;
    });
  }

  limpiar() {
    this.form.reset();
    this.nombres.forEach(n => {
      const el = this.campo(n);
      el.readOnly = false; el.disabled = false;
      const c = el.closest(".campo");
      c.classList.remove("valido", "invalido");
      c.querySelector(".error").textContent = "";
    });
  }
}
