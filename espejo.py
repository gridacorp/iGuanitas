# espejo.py

import os
import pandas as pd
from tkinter import messagebox, filedialog
from espejo_cuadrado import read_excel_file, compare_excel_sheets
from espejo_rectangular import (
    read_text_file,
    read_docx_file,
    read_pdf_file,
    read_pptx_file,
    compare_word_frequency
)

cancelar = False  # bandera global

def read_file(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".csv", ".xlsx", ".xls", ".xlsb"):
        return read_excel_file(path)  # dict: hoja→DataFrame
    elif ext in (".txt", ".py"):
        return read_text_file(path)   # list[str]
    elif ext == ".docx":
        return read_docx_file(path)
    elif ext == ".pdf":
        return read_pdf_file(path)
    elif ext == ".pptx":
        return read_pptx_file(path)
    else:
        raise Exception(f"Extensión no soportada: {ext}")

def compare_files(files, status_label, progress_bar):
    global cancelar
    cancelar = False

    if len(files) < 2:
        messagebox.showerror("Error", "Selecciona al menos dos archivos para comparar.")
        return

    # Leer todos los archivos
    all_content = {}
    for f in files:
        try:
            all_content[f] = read_file(f)
        except Exception as e:
            all_content[f] = f"Error leyendo {os.path.basename(f)}: {e}"

    # Calcular total de tareas para la barra
    items = list(all_content.items())
    total_pairs = 0
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            c1, c2 = items[i][1], items[j][1]
            if isinstance(c1, dict) and isinstance(c2, dict):
                total_pairs += len(c1) * len(c2)
            else:
                total_pairs += 1

    if total_pairs == 0:
        messagebox.showerror("Error", "No hay elementos válidos para comparar.")
        return

    results = []
    current = 0

    # Comparación par a par
    for i in range(len(items)):
        f1, c1 = items[i]
        for j in range(i+1, len(items)):
            f2, c2 = items[j]

            # --- Caso hojas de cálculo ---
            if isinstance(c1, dict) and isinstance(c2, dict):
                for hoja1, df1 in c1.items():
                    for hoja2, df2 in c2.items():
                        if cancelar:
                            return
                        pct = compare_excel_sheets(df1, df2)
                        results.append({
                            "Archivo 1": os.path.basename(f1),
                            "Hoja 1": hoja1,
                            "Archivo 2": os.path.basename(f2),
                            "Hoja 2": hoja2,
                            "% Diferencia por celdas": pct,
                            "% Diferencia por palabras": "N/A"
                        })

                        current += 1
                        progress = current / total_pairs * 100
                        progress_bar['value'] = progress
                        status_label.config(text=f"Comparando {current}/{total_pairs} hojas...")
                        status_label.update()
                        progress_bar.update()

            # --- Caso texto / docx / pdf / pptx ---
            else:
                if cancelar:
                    return
                l1 = c1 if isinstance(c1, list) else []
                l2 = c2 if isinstance(c2, list) else []
                pct_words = compare_word_frequency(l1, l2)
                results.append({
                    "Archivo 1": os.path.basename(f1),
                    "Hoja 1": "-",
                    "Archivo 2": os.path.basename(f2),
                    "Hoja 2": "-",
                    "% Diferencia por celdas": "N/A",
                    "% Diferencia por palabras": pct_words
                })

                current += 1
                progress = current / total_pairs * 100
                progress_bar['value'] = progress
                status_label.config(text=f"Comparando {current}/{total_pairs} archivos...")
                status_label.update()
                progress_bar.update()

    # Mostrar resultados
    summary = "\n".join(
        f"{r['Archivo 1']} ({r['Hoja 1']}) vs {r['Archivo 2']} ({r['Hoja 2']}) → "
        + (
            f"Celdas: {r['% Diferencia por celdas']}%"
            if r['% Diferencia por celdas'] != "N/A"
            else f"Palabras: {r['% Diferencia por palabras']}%"
        )
        for r in results
    )
    messagebox.showinfo("Resultado de comparación", summary)

    # Guardar CSV
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV", "*.csv")],
        title="Guardar resultados como CSV"
    )
    if save_path:
        pd.DataFrame(results).to_csv(save_path, index=False, encoding="utf-8")
        messagebox.showinfo("Guardado", f"Resultados guardados en:\n{save_path}")

    status_label.config(text="Comparación completada.")
    progress_bar['value'] = 100
