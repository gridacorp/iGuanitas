# telemetry.py

import os
import uuid
import urllib.request
import json
import platform
import locale
from datetime import datetime

from config import APP_VERSION   # ← Importamos la versión única

# ——————————————————————————————————————————————————————————————
# DATOS PERMITIDOS POR LICENCIA
#
# Dato                              ¿Permitido?  Comentario
# ✅ UUID de instalación             ✔️ Sí         Ya lo usas con .install_id o uid.dat
# ✅ Versión de la app               ✔️ Sí         Se toma de config.APP_VERSION
# ✅ Marca de tiempo de arranque     ✔️ Sí         Se interpreta como fecha/hora de ejecución
# ✅ Sistema operativo               ✔️ Sí         platform.system() + platform.version()
# ✅ Idioma del sistema              ✔️ Sí         locale.getdefaultlocale()
# ✅ Zona horaria                    ✔️ Sí         datetime.now().astimezone().tzname()
# ✅ IP aproximada para geolocalización ✔️ Sí      Sólo país y región (no guardar IP entera)
# ——————————————————————————————————————————————————————————————

MEASUREMENT_ID = "G-ZBK5TL76CR"
API_SECRET     = "VfSLIu4ESOyMPrtwzvaOMQ"

# URL de geolocalización anónima (devuelve JSON con country, region, etc.)
GEO_IP_URL     = "https://ipinfo.io/json"

def get_uid_path():
    local_appdata = os.getenv('LOCALAPPDATA')
    folder = os.path.join(local_appdata, "iGuanitas")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "uid.dat")

def get_or_create_uid():
    path = get_uid_path()
    try:
        with open(path, "r") as f:
            uid = f.read().strip()
            if uid:
                return uid
    except FileNotFoundError:
        pass
    new_uid = str(uuid.uuid4())
    with open(path, "w") as f:
        f.write(new_uid)
    return new_uid

def fetch_geo_info():
    """Devuelve sólo country y region, sin exponer la IP completa."""
    try:
        req = urllib.request.Request(GEO_IP_URL, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode())
            return {
                "country": data.get("country"),
                "region": data.get("region")
            }
    except Exception:
        return {"country": None, "region": None}

def ping_ga_event(event_name: str, params: dict = None):
    """Envía silenciosamente un evento personalizado a GA4."""
    client_id = get_or_create_uid()
    url = (
        f"https://www.google-analytics.com/mp/collect"
        f"?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}"
    )
    event = {"name": event_name}
    if params:
        event["params"] = params
    payload = {
        "client_id": client_id,
        "events": [event]
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass  # Silencioso

def ping_ga_startup():
    """Recolecta los datos permitidos y envía el evento 'app_start' a GA4."""
    # 1) UID y versión
    uid = get_or_create_uid()
    version = APP_VERSION

    # 2) Timestamp de arranque (UTC ISO8601)
    ts = datetime.utcnow().isoformat() + "Z"

    # 3) OS
    os_info = f"{platform.system()} {platform.version()}"

    # 4) Idioma
    lang, _ = locale.getdefaultlocale()

    # 5) Zona horaria
    tz = datetime.now().astimezone().tzname()

    # 6) Geolocalización aproximada
    geo = fetch_geo_info()

    params = {
        "install_id":   uid,
        "launch_timestamp": ts,
        "version":      version,
        "os":           os_info,
        "lang":         lang,
        "timezone":     tz,
        "country":      geo.get("country"),
        "region":       geo.get("region"),
    }

    ping_ga_event("app_start", params)
