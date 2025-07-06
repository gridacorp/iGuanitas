# telemetry.py

import os
import uuid
import urllib.request
import json

# Credenciales de Google Analytics 4
MEASUREMENT_ID = "G-ZBK5TL76CR"
API_SECRET     = "VfSLIu4ESOyMPrtwzvaOMQ"

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

def ping_ga_event(event_name: str):
    """Envía silenciosamente un evento personalizado a GA4."""
    client_id = get_or_create_uid()
    url = (
        f"https://www.google-analytics.com/mp/collect"
        f"?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}"
    )
    payload = {
        "client_id": client_id,
        "events": [{"name": event_name}]
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
        pass

def ping_ga_startup():
    """Envía el evento 'app_start' a GA4."""
    ping_ga_event("app_start")
