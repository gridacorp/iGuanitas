# espejo.py

import os
import pandas as pd
import numpy as np
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation
import openpyxl
import pytesseract
from pdf2image import convert_from_path

from iGuanitas import read_file, compare_lists, cancelar

def compare_files(files, status_label, progress_bar):
    global cancelar
    cancelar = False

    if len(files) < 2:
        messagebox.showerror("Error", "Selecciona al menos dos archivos para comparar.")
        return

    total = (len(files) * (len(files) - 1)) // 2
    current = 0
    results = []

    for i in range(len(files)):
        if cancelar:
            status_label.config(text="Proceso cancelado.")
            return
        a = files[i]
        try:
            data_a = read_file(a)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            continue

        for j in range(i + 1, len(files)):
            if cancelar:
                status_label.config(text="Proceso cancelado.")
                return
            b = files[j]
            try:
                data_b = read_file(b)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                continue

            current += 1
            status_label.config(
                text=f"Revisando {current}/{total}\n'{os.path.basename(a)}' vs '{os.path.basename(b)}'"
            )
            progress_bar["value"] = (current / total) * 100
            status_label.update_idletasks()
            progress_bar.update_idletasks()

            if isinstance(data_a, pd.DataFrame):
                df1, df2 = data_a.copy(), data_b.copy()
                mr, mc = max(df1.shape[0], df2.shape[0]), max(df1.shape[1], df2.shape[1])
                df1 = df1.reindex(index=range(mr), columns=range(mc), fill_value=np.nan)
                df2 = df2.reindex(index=range(mr), columns=range(mc), fill_value=np.nan)
                ch = (df1 != df2) & ~(df1.isna() & df2.isna())
                pct = round((ch.sum().sum() / (mr * mc)) * 100, 2)
            else:
                pct = compare_lists(data_a, data_b)

            results.append([os.path.basename(a), os.path.basename(b), pct])

    save = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    if save:
        pd.DataFrame(results, columns=["Archivo 1", "Archivo 2", "% Diferencia"]) \
          .to_csv(save, index=False, encoding="utf-8")
        messagebox.showinfo("Listo", f"Guardado en {save}")

    status_label.config(text="Comparación completada.")
    progress_bar["value"] = 100