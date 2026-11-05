class Dom {
  static id(id) { return document.getElementById(id); }

  static esc(s) {
    const d = document.createElement("div");
    d.textContent = s ?? "";
    return d.innerHTML;
  }
}

class Notificador {
  static mostrar(msg, tipo = "ok") {
    const t = document.createElement("div");
    t.className = "toast " + (tipo === "error" ? "error" : "");
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
  }
}

// Cliente de la API REST
class ApiClient {
  static async peticion(url, method = "GET", body = null) {
    const opts = { method, headers: {} };
    if (body !== null) {
      opts.headers["Content-Type"] = "application/json";
      opts.body = JSON.stringify(body);
    }
    const r = await fetch(url, opts);
    let data = null;
    if (r.status !== 204) { try { data = await r.json(); } catch (e) { /* sin cuerpo */ } }
    if (r.status === 401) location.href = "/login";
    return { ok: r.ok, status: r.status, data };
  }

  static get(url) { return ApiClient.peticion(url, "GET"); }
  static post(url, body) { return ApiClient.peticion(url, "POST", body); }
  static put(url, body) { return ApiClient.peticion(url, "PUT", body); }
  static patch(url, body) { return ApiClient.peticion(url, "PATCH", body); }
  static delete(url) { return ApiClient.peticion(url, "DELETE"); }
}

class Menu {
  iniciar() {
    Dom.id("burger")?.addEventListener("click", () => Dom.id("menu").classList.toggle("abierto"));
  }
}

new Menu().iniciar();
