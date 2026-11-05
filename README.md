# Ticket de Turno

Aplicación web para solicitar turnos de atención, con parte pública y panel de administración.

**Materia:** Desarrollo de Aplicaciones Web (Parcial 2)

## Tecnologías

- **Backend:** Python 3 + Flask (sin PHP)
- **ORM:** SQLAlchemy (Flask-SQLAlchemy)
- **Base de datos:** SQLite (se crea sola al arrancar)
- **Frontend:** HTML, CSS y JavaScript (clases ES6), Chart.js para las gráficas
- **Arquitectura:** MVC + capa de servicios, totalmente orientada a objetos
- **Patrones de diseño:** Factory (`TicketFactory`), Singleton (`PdfService`) y Application Factory (`Aplicacion`)
- **API:** REST en `/api/v1/...`

## Requisitos

- Windows 10 u 11
- Python 3.10 o superior

Para instalar Python: descárgalo de https://www.python.org/downloads/ y **marca la casilla "Add python.exe to PATH"** durante la instalación.

Verifica la instalación abriendo PowerShell:

```powershell
python --version
```

## Instalación y ejecución (PowerShell)

1. Descomprime el ZIP y abre PowerShell dentro de la carpeta del proyecto (clic derecho en la carpeta > "Abrir en Terminal", o `cd` hasta ella).

2. Crea el entorno virtual:

```powershell
python -m venv venv
```

3. Actívalo:

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecución de scripts, corre esto una vez y vuelve a activar:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Si usas CMD en lugar de PowerShell, el comando es `venv\Scripts\activate.bat`.

4. Instala las dependencias:

```powershell
pip install -r requirements.txt
```

5. Arranca el servidor:

```powershell
python run.py
```

6. Abre el navegador en `http://localhost:5000`

Para detener el servidor presiona `Ctrl + C`. Para volver a ejecutarlo en otra sesión basta con activar el entorno (paso 3) y correr `python run.py`.

## Accesos

| Parte | URL | Credenciales |
|---|---|---|
| Pública (solicitar turno) | http://localhost:5000 | Sin login |
| Modificar turno | http://localhost:5000/modificar | CURP + número de turno |
| Administrador | http://localhost:5000/login | usuario `admin`, contraseña `admin123` + captcha |

La base de datos y el usuario administrador se crean automáticamente la primera vez. Los catálogos (municipios, niveles y asuntos) vienen con datos de ejemplo y se administran desde el panel.

## Datos de prueba

CURP de ejemplo con formato válido: `GOMC900101HCLRRS09`
Para más solicitudes, cambia algunos dígitos: `GOMC900102HCLRRS01`

## Funcionalidades

**Parte pública**
- Solicitud de turno con validación de datos en el navegador y en el servidor.
- El turno inicia en 1 por cada municipio y lleva su propio control.
- Comprobante en PDF con código QR (contiene la CURP del alumno) y código de barras.
- Modificación de la solicitud con CURP + número de turno.

**Parte privada (administrador)**
- Login con usuario, contraseña y captcha.
- Consulta por CURP o nombre, con filtros por estatus y municipio.
- Registrar, modificar y eliminar solicitudes, y marcarlas como "Pendiente" o "Resuelto".
- CRUD de catálogos: municipios, niveles y asuntos.
- Dashboard con gráficas de estatus, filtrable por total de solicitudes o por municipio.
- Menú de navegación y cierre de sesión.

## Estructura del proyecto
