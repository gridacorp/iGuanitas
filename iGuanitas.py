import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading
import webbrowser
import urllib.request
import urllib.error
import ctypes

# Fijar AppUserModelID para que Windows muestre el icono correctamente en la barra de tareas
def set_app_user_model_id():
    myappid = 'gridacorp.iGuanitas.1'
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

import espejo
from license import show_license_and_get_acceptance
from metadatos import mostrar_metadatos
from acerca_de import mostrar_acerca_de
from telemetry import ping_ga_startup, ping_ga_event
from config import APP_VERSION as LOCAL_VERSION  # ← Importamos la versión única

# ------------ Configuración de actualización ------------
VERSION_URL = (
    "https://raw.githubusercontent.com/gridacorp/iGuanitas/main/version.txt"
)
DOWNLOAD_URL = (
    "https://raw.githubusercontent.com/gridacorp/iGuanitas/main/download_url.txt"
)

def check_for_update_bloqueante(root):
    """
    Comprueba si hay una nueva versión remota. Si existe, muestra un mensaje bloqueante,
    abre el enlace de descarga y cierra la aplicación actual.
    """
    try:
        with urllib.request.urlopen(VERSION_URL) as response:
            remote_version = response.read().decode('utf-8').strip()

        if remote_version > LOCAL_VERSION:
            with urllib.request.urlopen(DOWNLOAD_URL) as resp2:
                download_link = resp2.read().decode('utf-8').strip()

            def mostrar_mensaje():
                messagebox.showinfo(
                    "¡Actualización obligatoria!",
                    f"Se ha lanzado una nueva versión ({remote_version}).\n"
                    "Debes actualizar para continuar. Se abrirá el navegador para descargarla."
                )
                webbrowser.open(download_link)
                root.destroy()

            root.after(0, mostrar_mensaje)
    except Exception as e:
        print(f"Error comprobando actualizaciones: {e}")

def main():
    # 0) Establecer AppUserModelID antes de crear la ventana
    set_app_user_model_id()

    # 1) Mostrar licencia y esperar aceptación
    if not show_license_and_get_acceptance():
        return

    # 2) Crear ventana principal oculta para comprobación de actualización
    root = tk.Tk()

    # 🧩 Establecer icono para ventana y barra de tareas
    try:
        img = tk.PhotoImage(file='icono.ico')
        root.tk.call('wm', 'iconphoto', root._w, img)
    except Exception:
        pass

    root.withdraw()
    check_for_update_bloqueante(root)
    root.deiconify()

    # 3) Lanzar telemetría de arranque en segundo plano
    threading.Thread(target=ping_ga_startup, daemon=True).start()

    # Configuración de interfaz
    root.title(f"iGuanitas Community 🦎 - Comparador de Archivos v{LOCAL_VERSION}")
    root.geometry("600x750")
    root.configure(bg="#F5F5F5")

    header_font    = ("Arial", 18, "bold")
    subheader_font = ("Arial", 13, "bold")
    btn_font       = ("Arial", 14, "bold")
    botones = []

    tk.Label(root, text="🦎 iGuanitas Community", font=header_font,
             fg="#2E8B57", bg="#F5F5F5").pack(pady=(20,10))
    tk.Label(root, text="Selecciona el tipo de archivo que deseas comparar:",
             font=subheader_font, bg="#F5F5F5").pack(pady=(0,15))

    status_label = tk.Label(root, text="", fg="#1E90FF", font=("Arial",11),
                            wraplength=560, justify="center", bg="#F5F5F5")
    status_label.pack(pady=5)
    progress_bar = ttk.Progressbar(root, length=540, mode='determinate')
    progress_bar.pack(pady=(0,15))

    btn_specs = [
        ("🦎 📊 Comparar Hojas de Cálculo", ("*.xlsx","*.xls","*.xlsb","*.csv")),
        ("🦎 📄 Comparar Archivos de Texto", ("*.txt","*.py")),
        ("🦎 📝 Comparar Documentos Word",   ("*.doc","*.docx")),
        ("🦎 📕 Comparar Archivos PDF",     ("*.pdf",)),
        ("🦎 📽 Comparar Presentaciones",   ("*.pptx",)),
    ]

    for text, exts in btn_specs:
        def _pick_and_compare(t=text, e=exts):
            files = filedialog.askopenfilenames(filetypes=[(t,e)])
            if files:
                status_label.config(text="Procesando comparación...")
                for b in botones: b.config(state=tk.DISABLED)
                def run_and_reenable():
                    espejo.compare_files(files, status_label, progress_bar)
                    for b in botones: b.config(state=tk.NORMAL)
                    status_label.config(text="")
                threading.Thread(target=run_and_reenable, daemon=True).start()

        btn = tk.Button(root, text=text, width=42, font=btn_font,
                        bg="#DFFFE0", activebackground="#C8F7C5",
                        command=_pick_and_compare)
        btn.pack(pady=6)
        botones.append(btn)

    tk.Label(root, text="", bg="#F5F5F5").pack(pady=5)

    btn_meta = tk.Button(
        root,
        text="🦎 🔍 Comparar Propiedades / Hash",
        width=42, font=btn_font, bg="#E6F0FF",
        activebackground="#D0E4FF",
        command=lambda: mostrar_metadatos(root)
    )
    btn_meta.pack(pady=10)
    botones.append(btn_meta)

    tk.Button(
        root,
        text="🦎 ❌ Cancelar Comparación",
        width=42, font=btn_font,
        bg="#FFD6D6", activebackground="#FFC0C0",
        command=lambda: setattr(espejo, 'cancelar', True)
    ).pack(pady=5)

    tk.Label(root, text="", bg="#F5F5F5").pack(pady=5)

    def _show_about_and_ping():
        ping_ga_event("about_open")
        mostrar_acerca_de()

    btn_about = tk.Button(
        root,
        text="🦎 ℹ️ Acerca de iGuanitas",
        width=42, font=btn_font, bg="#FFFACD",
        activebackground="#FFF3A0",
        command=_show_about_and_ping
    )
    btn_about.pack(pady=(10,5))
    botones.append(btn_about)

    def abrir_paypal():
        webbrowser.open("https://www.paypal.com/donate/?hosted_button_id=KQZ5A7HXTULZL")

    boton_donar = tk.Button(
        root,
        text="🦎 💖 Donar con PayPal",
        command=abrir_paypal,
        bg="#0070BA", fg="white",
        padx=10, pady=5,
        font=btn_font
    )
    boton_donar.pack(pady=10)
    botones.append(boton_donar)

    root.mainloop()

if __name__ == "__main__":
    main()
