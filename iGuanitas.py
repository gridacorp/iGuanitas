# iGuanitas.py

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading
import espejo  # módulo con compare_files y bandera cancelar

from license import show_license_and_get_acceptance
from espejo import compare_files
from metadatos import mostrar_metadatos

def mostrar_acerca_de():
    """Muestra un diálogo con información del programa."""
    messagebox.showinfo(
        "Acerca de",
        "iGuanitas v1.0\nDesarrollado por TuNombre\n© 2025"
    )

def main():
    # 1) Mostrar la licencia al inicio
    if not show_license_and_get_acceptance():
        return

    # 2) Crear ventana principal
    root = tk.Tk()
    root.title("iGuanitas - Comparador de Archivos")
    root.geometry("600x660")

    # 3) Encabezado
    tk.Label(
        root,
        text="Selecciona qué tipo de documento comparar:",
        font=("Arial", 12)
    ).pack(pady=10)

    # 4) Estado y barra de progreso
    status_label = tk.Label(
        root, text="", fg="blue", font=("Arial", 10),
        wraplength=580, justify="center"
    )
    status_label.pack(pady=5)
    progress_bar = ttk.Progressbar(root, length=550, mode='determinate')
    progress_bar.pack(pady=5)

    # 5) Botones para cada tipo de archivo
    btn_specs = [
        ("📊 Hojas de cálculo", "*.xlsx *.xls *.xlsb *.csv"),
        ("📄 Texto plano",      "*.txt *.py"),
        ("📝 Word",             "*.doc *.docx"),
        ("📕 PDF",              "*.pdf"),
        ("📽 PowerPoint",       "*.ppt *.pptx"),
    ]
    for text, exts in btn_specs:
        def _pick_and_compare(t=text, e=exts):
            files = filedialog.askopenfilenames(filetypes=[(t, e)])
            if files:
                threading.Thread(
                    target=compare_files,
                    args=(files, status_label, progress_bar),
                    daemon=True
                ).start()

        tk.Button(
            root,
            text=f"{text} ({exts})",
            width=60,
            command=_pick_and_compare
        ).pack(pady=3)

    # 6) Botón para metadatos y hash
    tk.Button(
        root,
        text="🔍 Comparar Propiedades y Hash",
        width=60,
        command=lambda: mostrar_metadatos(root)
    ).pack(pady=15)

    # 7) Botón para cancelar el proceso en curso
    tk.Button(
        root,
        text="❌ Cancelar proceso",
        bg="red", fg="white",
        width=60,
        command=lambda: setattr(espejo, 'cancelar', True)
    ).pack(pady=5)

    # 8) Botón "Acerca de"
    tk.Button(
        root,
        text="ℹ️ Acerca de",
        width=60,
        command=mostrar_acerca_de
    ).pack(pady=10)

    # 9) Iniciar loop de la GUI
    root.mainloop()

if __name__ == "__main__":
    main()

