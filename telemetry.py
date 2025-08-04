import os
import urllib.request
import json
import platform
import locale
from datetime import datetime
from pathlib import Path
import webbrowser

from config import APP_VERSION   # ← Importamos la versión única
from install_id import get_install_id  # Reutilizamos el UUID de instalación

# ——————————————————————————————————————————————————————————————
# DATOS PERMITIDOS POR LICENCIA
#
# Dato                              ¿Permitido?  Comentario
# ✅ UUID de instalación             ✔️ Sí         Se toma de install_id.get_install_id()
# ✅ Versión de la app               ✔️ Sí         Se toma de config.APP_VERSION
# ✅ Marca de tiempo de arranque     ✔️ Sí         Fecha/hora de ejecución
# ✅ Sistema operativo               ✔️ Sí         platform.system() + platform.version()
# ✅ Idioma del sistema              ✔️ Sí         locale.getdefaultlocale()
# ✅ Zona horaria                    ✔️ Sí         datetime.now().astimezone().tzname()
# ✅ IP aproximada para geolocalización ✔️ Sí      Sólo país y región (no guardar IP completa)
# ——————————————————————————————————————————————————————————————

MEASUREMENT_ID = "G-ZBK5TL76CR"
API_SECRET     = "VfSLIu4ESOyMPrtwzvaOMQ"
DONATION_URL   = "https://www.paypal.com/donate/?hosted_button_id=KQZ5A7HXTULZL"

# Archivo para contar número de ejecuciones
tmp_dir = os.getenv('LOCALAPPDATA') or str(Path.home())
COUNT_FILE = Path(tmp_dir) / "iGuanitas" / "exec_count.dat"
COUNT_FILE.parent.mkdir(parents=True, exist_ok=True)


def fetch_geo_info():
    """Devuelve sólo country y region, sin exponer la IP completa."""
    try:
        req = urllib.request.Request("https://ipinfo.io/json", headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            return {"country": data.get("country"), "region": data.get("region")}
    except Exception:
        return {"country": None, "region": None}


def ping_ga_event(event_name: str, params: dict = None):
    """Envía silenciosamente un evento personalizado a GA4."""
    client_id = get_install_id()
    url = (
        f"https://www.google-analytics.com/mp/collect"
        f"?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}"
    )
    event = {"name": event_name}
    if params:
        event["params"] = params
    payload = {"client_id": client_id, "events": [event]}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass  # Silencioso


def _increment_execution_count() -> int:
    """Lee, incrementa y persiste el contador de ejecuciones."""
    try:
        count = int(COUNT_FILE.read_text())
    except Exception:
        count = 0
    count += 1
    COUNT_FILE.write_text(str(count))
    return count


def ping_ga_startup():
    """Recolecta los datos permitidos y envía el evento 'app_start' a GA4. Abre enlace de donación cada 5 arranques."""
    # Incrementar contador de ejecuciones y abrir PayPal cada 5
    count = _increment_execution_count()
    if count % 5 == 0:
        webbrowser.open(DONATION_URL)

    # 1) UID y versión
    uid = get_install_id()
    version = APP_VERSION

    # 2) Timestamp de arranque (UTC ISO8601)
    ts = datetime.utcnow().isoformat() + "Z"

    # 3) OS
    os_info = f"{platform.system()} {platform.version()}"

    # 4) Idioma
    lang, _ = locale.getdefaultlocale() or (None, None)

    # 5) Zona horaria
    tz = datetime.now().astimezone().tzname()

    # 6) Geolocalización aproximada
    geo = fetch_geo_info()

    params = {
        "install_id":       uid,
        "launch_timestamp": ts,
        "version":          version,
        "os":               os_info,
        "lang":             lang,
        "timezone":         tz,
        "country":          geo.get("country"),
        "region":           geo.get("region"),
        "run_count":        count
    }

    ping_ga_event("app_start", params)
