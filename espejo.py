# espejo.py

import os
import pandas as pd
import numpy as np
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation
import openpyxl

cancelar = False  # bandera global para cancelar proceso

def read_file(path):
    """Lee el contenido del archivo y devuelve DataFrame o lista."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xls", ".xlsb", ".csv"):
        try:
            if ext == ".csv":
                return pd.read_csv(path)
            else:
                return pd.read_excel(path)
        except Exception as e:
            raise Exception(f"Error leyendo {path}: {e}")
    elif ext in (".txt", ".py"):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()
    elif ext in (".docx",):
        doc = Document(path)
        return [p.text for p in doc.paragraphs]
    elif ext in (".pdf",):
        # Solo texto plano (más completo necesita OCR o pdfminer)
        try:
            r = PdfReader(path)
            text = []
            for page in r.pages:
                text.append(page.extract_text())
            return text
        except Exception as e:
            raise Exception(f"Error leyendo PDF {path}: {e}")
    elif ext in (".pptx",):
        prs = Presentation(path)
        text = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text.append(shape.text)
        return text
    else:
        raise Exception(f"Extensión no soportada para comparación: {ext}")

def compare_lists(list1, list2):
    """Compara dos listas línea a línea y devuelve porcentaje de diferencia."""
    max_len = max(len(list1), len(list2))
    if max_len == 0:
        return 0.0
    diffs = sum(1 for a, b in zip(list1, list2) if a != b)
    # Contar líneas extra que no coinciden
    diffs += abs(len(list1) - len(list2))
    return round((diffs / max_len) * 100, 2)

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
            status_label.config(text="Proceso cancelado
