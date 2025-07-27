# install_id.py

import os
import uuid

# Archivo donde se guarda el UUID de instalación
_ID_FILE = os.path.join(os.getenv('LOCALAPPDATA', os.getcwd()), "iGuanitas", "install_id.dat")

def _ensure_folder():
    folder = os.path.dirname(_ID_FILE)
    os.makedirs(folder, exist_ok=True)

def get_install_id() -> str:
    """Lee o crea un UUID persistente para esta instalación."""
    _ensure_folder()
    try:
        with open(_ID_FILE, "r") as f:
            uid = f.read().strip()
            if uid:
                return uid
    except FileNotFoundError:
        pass

    uid = str(uuid.uuid4())
    with open(_ID_FILE, "w") as f:
        f.write(uid)
    return uid
