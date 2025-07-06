# iGuanitas.py

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import threading

import espejo                        # Tu módulo con compare_files y la variable cancelar
from license import show_license_and_get_acceptance
from metadatos import mostrar_metadatos
from acerca_de import mostrar_acerca_de


def main():
    # 1) Mostrar licencia
    if not show_license_and_get_acceptance():
        return

    # 2) Ventana principal
    root = tk.Tk()
    root.title("iGuanitas Community 🦎 - Comparador de Archivos")
    root.geometry("600x750")
    root.configure(bg="#F5F5F5")

    # Fuentes
    header_font = ("Arial", 18, "bold")
    subheader_font = ("Arial", 13, "bold")
    btn_font = ("Arial", 14, "bold")

    botones = []

    # 3) Encabezado
    tk.Label(
        root,
        text="🦎 iGuanitas Community",
        font=header_font,
        fg="#2E8B57",
        bg="#F5F5F5"
    ).pack(pady=(20, 10))

    tk.Label(
        root,
        text="Selecciona el tipo de archivo que deseas comparar:",
        font=subheader_font,
        bg="#F5F5F5"
    ).pack(pady=(0, 15))

    # 4) Estado y progreso
    status_label = tk.Label(
        root,
        text="",
        fg="#1E90FF",
        font=("Arial", 11),
        wraplength=560,
        justify="center",
        bg="#F5F5F5"
    )
    status_label.pack(pady=5)

    progress_bar = ttk.Progressbar(root, length=540, mode='determinate')
    progress_bar.pack(pady=(0, 15))

    # 5) Botones de tipo de archivo
    btn_specs = [
        ("🦎 📊 Comparar Hojas de Cálculo", ("*.xlsx", "*.xls", "*.xlsb", "*.csv")),
        ("🦎 📄 Comparar Archivos de Texto", ("*.txt", "*.py")),
        ("🦎 📝 Comparar Documentos Word",   ("*.doc", "*.docx")),
        ("🦎 📕 Comparar Archivos PDF",     ("*.pdf",)),
        ("🦎 📽 Comparar Presentaciones",   ("*.ppt", "*.pptx")),
    ]

    for text, exts in btn_specs:
        def _pick_and_compare(t=text, e=exts):
            files = filedialog.askopenfilenames(filetypes=[(t, e)])
            if files:
                status_label.config(text="Procesando comparación...")
                for b in botones:
                    b.config(state=tk.DISABLED)

                def run_and_reenable():
                    espejo.compare_files(files, status_label, progress_bar)
                    for b in botones:
                        b.config(state=tk.NORMAL)
                    status_label.config(text="")

                threading.Thread(target=run_and_reenable, daemon=True).start()

        btn = tk.Button(
            root,
            text=text,
            width=42,
            font=btn_font,
            bg="#DFFFE0",
            activebackground="#C8F7C5",
            relief=tk.RAISED,
            command=_pick_and_compare
        )
        btn.pack(pady=6)
        botones.append(btn)

    # Separador visual
    tk.Label(root, text="", bg="#F5F5F5").pack(pady=5)

    # 6) Botón Metadatos
    btn_meta = tk.Button(
        root,
        text="🦎 🔍 Comparar Propiedades / Hash",
        width=42,
        font=btn_font,
        bg="#E6F0FF",
        activebackground="#D0E4FF",
        command=lambda: mostrar_metadatos(root)
    )
    btn_meta.pack(pady=10)
    botones.append(btn_meta)

    # 7) Botón Cancelar proceso
    tk.Button(
        root,
        text="🦎 ❌ Cancelar Comparación",
        width=42,
        font=btn_font,
        bg="#FFD6D6",
        activebackground="#FFC0C0",
        command=lambda: setattr(espejo, 'cancelar', True)
    ).pack(pady=5)

    # Separador visual
    tk.Label(root, text="", bg="#F5F5F5").pack(pady=5)

    # 8) Botón Acerca de
    btn_about = tk.Button(
        root,
        text="🦎 ℹ️ Acerca de iGuanitas",
        width=42,
        font=btn_font,
        bg="#FFFACD",
        activebackground="#FFF3A0",
        command=mostrar_acerca_de
    )
    btn_about.pack(pady=(10, 25))
    botones.append(btn_about)

    # 9) Iniciar la aplicación
    root.mainloop()


if __name__ == "__main__":
    main()
