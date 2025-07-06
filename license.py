# license.py

import tkinter as tk
import os
import uuid

# --- Generación y almacenamiento de ID de instalación único ---
# Se guarda en un archivo oculto junto al script para persistir entre ejecuciones.
ID_FILE = os.path.join(os.path.dirname(__file__), '.install_id')
try:
    if os.path.exists(ID_FILE):
        with open(ID_FILE, 'r') as f:
            INSTALL_ID = f.read().strip()
    else:
        INSTALL_ID = str(uuid.uuid4())
        with open(ID_FILE, 'w') as f:
            f.write(INSTALL_ID)
except Exception:
    INSTALL_ID = 'UNKNOWN'

# Tu texto de licencia completo:
LICENSE_TEXT = r"""
iGuanitas Source-Available No Comercial License v1.0

Copyright (C) 2025 Jose Antonio Sifuentes Maltos

Todos tienen permiso para copiar y distribuir copias literales de este documento de licencia, pero no está permitido modificarlo.

PREÁMBULO
Este documento establece los términos de la Licencia Pública General Affero GNU versión 3, adaptada y reforzada con restricciones de uso comercial y disposiciones de telemetría y privacidad. El propósito es garantizar la libertad de usar, estudiar, compartir y modificar el software, al mismo tiempo que se prohíbe expresamente cualquier explotación comercial sin una licencia escrita separada otorgada por el Autor.

TÉRMINOS Y CONDICIONES

0. DEFINICIONES
   a) Software: el código fuente, binarios, documentación, datos, scripts, interfaces, materiales visuales y cualquier trabajo derivado.
   b) Tú (o Licenciatario): la persona o entidad que ejerce derechos bajo esta licencia.
   c) Uso Comercial: cualquier uso que genere ingresos o beneficios económicos, reduzca costos en actividades con fines de lucro o implique integración en productos o servicios con ánimo de lucro.
   d) Uso No Comercial: uso exclusivamente personal, doméstico, educativo, académico, de investigación o en organizaciones sin fines de lucro.
   e) Propagar y Convey: significados dados en las Secciones 1 y 5 de la AGPLv3.
   f) AGPLv3: GNU Affero General Public License versión 3.

1. CÓDIGO FUENTE
   El Código Fuente Correspondiente incluye todo el código fuente necesario para generar, instalar y ejecutar el código objeto y modificar el trabajo, incluidos los scripts de control de reparación y actualización.

2. PERMISOS BÁSICOS
   Tienes permiso para ejecutar, propagar y modificar el software para Uso No Comercial, sujeto a las restricciones de la Sección 6.

3. PROTECCIÓN CONTRA LEYES DE CIRCUNVENCIÓN
   Ningún trabajo cubierto se considerará parte de una medida efectiva de protección tecnológica bajo la ley aplicable.

4. OBLIGACIONES AL PROPAGAR
   a) Disponibilidad del código fuente: Debes poner a disposición el Código Fuente Correspondiente bajo los términos de esta licencia.
   b) Uso en red: Si modificas el software y lo ejecutas como servicio en red, debes ofrecer a todos los usuarios acceso al Código Fuente Correspondiente.

5. DISTRIBUCIÓN DE FORMAS NO FUENTE
   Puedes distribuir código objeto bajo los términos de la Sección 6 de la AGPLv3, siempre que cumplas con los requisitos de Uso No Comercial.

6. RESTRICCIÓN NO COMERCIAL
   a) Prohibición de Uso Comercial: No puedes usar, copiar, distribuir ni modificar el software con fines comerciales sin una licencia escrita separada del Autor.
   b) Solo Uso No Comercial: Cualquier uso más allá de los ámbitos personales, educativos o sin fines de lucro queda prohibido.
   c) Terminación automática: El incumplimiento de esta sección extingue inmediatamente tus derechos bajo esta licencia.

7. TERMINACIÓN
   Tus derechos bajo esta licencia se pierden si incumples cualquier término, especialmente el de la Sección 6. Podrán restaurarse si solucionas la infracción dentro de los 30 días siguientes a la notificación del Autor.

8. EXENCIÓN DE GARANTÍAS
   El software se proporciona TAL CUAL, sin garantías de ningún tipo, expresas o implícitas, incluidas garantías de comerciabilidad, idoneidad para un propósito particular o no infracción.

9. LIMITACIÓN DE RESPONSABILIDAD
   Bajo ninguna circunstancia el Autor será responsable de daños directos, indirectos, incidentales, especiales, punitivos o consecuentes derivados del uso o la imposibilidad de usar el software.

10. ACCESO AL CÓDIGO FUENTE EN COPIAS DISTRIBUIDAS
    Al distribuir el software en cualquier forma, debes proporcionar acceso al Código Fuente Correspondiente según esta licencia.

11. TELEMETRÍA Y PRIVACIDAD
    a) Finalidad: Con tu consentimiento expreso, el software enviará datos anónimos (UUID de instalación, versión, marca de tiempo de arranque, SO e idioma, zona horaria/IP aproximada) a un servicio de análisis.
    b) Datos no recolectados: No se recopilan datos personales identificables ni el contenido de documentos comparados.
    c) Uso: Datos utilizados exclusivamente para medir instalaciones, seguimiento de versiones y errores, y estadísticas geográficas agregadas.
    d) Consentimiento: Al ejecutar el software, consientes la telemetría. Puedes revocar el consentimiento desconectando Internet o eliminando %LOCALAPPDATA%\iGuanitas\uid.dat.
    e) Retención: La telemetría se almacena conforme a la política de privacidad del servicio analítico y no se comparte con terceros.

12. REVISIÓN DE LICENCIA
    El Autor puede publicar nuevas versiones de esta licencia. Puedes optar por adoptar nuevas versiones; ningún cambio obligatorio se aplicará sin al menos 90 días de aviso público previo.

FIN DE LA LICENCIA
"""

def show_license_and_get_acceptance():
    """Muestra el texto de la licencia en un diálogo y devuelve True si el usuario acepta."""
    dlg = tk.Tk()
    dlg.title("Licencia de Uso - iGuanitas")
    dlg.geometry("700x500")

    txt = tk.Text(dlg, wrap="word")
    txt.insert("1.0", LICENSE_TEXT)
    txt.config(state="disabled")
    txt.pack(fill=tk.BOTH, expand=True)

    accepted = tk.BooleanVar(value=False)
    def on_accept():
        accepted.set(True)
        dlg.destroy()
    def on_decline():
        dlg.destroy()

    frame = tk.Frame(dlg)
    tk.Button(frame, text="Acepto", command=on_accept, width=12).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(frame, text="No acepto", command=on_decline, width=12).pack(side=tk.LEFT, padx=5, pady=5)
    frame.pack()

    dlg.mainloop()
    return accepted.get()
