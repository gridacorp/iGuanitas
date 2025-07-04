# iGuanitas.py

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading

import espejo                        # tu módulo con compare_files y variable cancelar
from license import show_license_and_get_acceptance
from metadatos import mostrar_metadatos
from acerca_de import mostrar_acerca_de


def main():
    # 1) Mostrar la licencia al inicio
    if not show_license_and_get_acceptance():
        return

    # 2) Crear ventana principal
    root = tk.Tk()
    root.title("iGuanitas Community🦎 - Comparador de Archivos")
    root.geometry("600x700")

    # Fuente para botones: más grande y en negritas
    btn_font = ("Arial", 14, "bold")
    header_font = ("Arial", 16, "bold")

    # 3) Encabezado con nombre del programa
    tk.Label(
        root,
        text="🦎 Bienvenido a iGuanitas Community🦎",
        font=header_font,
        fg="#2E8B57"
    ).pack(pady=10)

    tk.Label(
        root,
        text="Selecciona qué tipo de documento comparar:",
        font=("Arial", 12)
    ).pack(pady=5)

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
        ("🦎 📊 Hojas de cálculo", ("*.xlsx", "*.xls", "*.xlsb", "*.csv")),
        ("🦎 📄 Texto plano",      ("*.txt", "*.py")),
        ("🦎 📝 Word",             ("*.doc", "*.docx")),
        ("🦎 📕 PDF",              ("*.pdf",)),
        ("🦎 📽 PowerPoint",       ("*.ppt", "*.pptx")),
    ]
    for text, exts in btn_specs:
        def _pick_and_compare(t=text, e=exts):
            files = filedialog.askopenfilenames(filetypes=[(t, e)])
            if files:
                threading.Thread(
                    target=espejo.compare_files,
                    args=(files, status_label, progress_bar),
                    daemon=True
                ).start()

        tk.Button(
            root,
            text=text,
            width=40,
            font=btn_font,
            bg="#E0FFE0",
            command=_pick_and_compare
        ).pack(pady=8)

    # 6) Botón para metadatos y hash
    tk.Button(
        root,
        text="🦎 🔍 Comparar Propiedades y Hash",
        width=40,
        font=btn_font,
        bg="#E0FFE0",
        command=lambda: mostrar_metadatos(root)
    ).pack(pady=10)

    # 7) Botón para cancelar el proceso
    tk.Button(
        root,
        text="🦎 ❌ Cancelar proceso",
        width=40,
        font=btn_font,
        bg="#FFCCCC", fg="black",
        command=lambda: setattr(espejo, 'cancelar', True)
    ).pack(pady=5)

    # 8) Botón “Acerca de”
    tk.Button(
        root,
        text="🦎 ℹ️ Acerca de",
        width=40,
        font=btn_font,
        bg="#E0FFE0",
        command=mostrar_acerca_de
    ).pack(pady=15)

    # 9) Iniciar loop de la GUI
    root.mainloop()


if __name__ == "__main__":
    main()
