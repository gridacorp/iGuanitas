# espejo_cuadrado.py

import os
import pandas as pd

def read_excel_file(path: str) -> dict:
    """
    Lee un archivo .csv, .xlsx, .xls o .xlsb y devuelve un dict
    {nombre_hoja: DataFrame}.
    """
    ext = os.path.splitext(path)[1].lower()
    base = os.path.splitext(os.path.basename(path))[0]

    if ext == ".csv":
        # tus dos intentos de lectura con distintos encodings...
        try:
            df = pd.read_csv(path, header=None, dtype=str,
                             encoding="utf-8", sep=None,
                             engine="python", on_bad_lines="skip")
        except UnicodeDecodeError:
            df = pd.read_csv(path, header=None, dtype=str,
                             encoding="latin-1", sep=None,
                             engine="python", on_bad_lines="skip")
        return {base: df}

    elif ext in (".xlsx", ".xls", ".xlsb"):
        sheets = pd.read_excel(path, sheet_name=None,
                               header=None, dtype=str)
        return sheets

    else:
        raise ValueError(f"Extensión no soportada por cuadrado: {ext}")


def compare_excel_sheets(df1: pd.DataFrame,
                         df2: pd.DataFrame) -> float:
    """
    Compara dos DataFrames (mismo tamaño tras reindexar con "") y
    devuelve el % de celdas distintas.
    """
    mr = max(df1.shape[0], df2.shape[0])
    mc = max(df1.shape[1], df2.shape[1])
    d1 = df1.reindex(index=range(mr),
                     columns=range(mc),
                     fill_value="").astype(str)
    d2 = df2.reindex(index=range(mr),
                     columns=range(mc),
                     fill_value="").astype(str)

    diff = (d1.values != d2.values)
    pct = round(diff.sum() / (mr * mc) * 100, 2)
    return pct
