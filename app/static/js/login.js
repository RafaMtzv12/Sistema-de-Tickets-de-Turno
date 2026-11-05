class LoginPage {
  iniciar() {
    Dom.id("btn-captcha").addEventListener("click", () => this.recargarCaptcha());
  }

  recargarCaptcha() {
    Dom.id("img-captcha").src = "/captcha.png?t=" + Date.now();
  }
}

new LoginPage().iniciar();
