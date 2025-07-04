#acerca_de.py

import tkinter as tk
from tkinter import messagebox
import os

def mostrar_acerca_de():
    # Obtener usuario y nombre del equipo
    try:
        usuario = os.getlogin()
    except Exception:
        usuario = "Usuario desconocido"
    equipo = os.environ.get('COMPUTERNAME', 'Equipo desconocido')

    texto = (
        "Sobre iGuanitas Source‑Available No Comercial License v1.0\n"
        "Copyright © 2025 Autor del software. Todos los derechos reservados.\n\n"
        "Esta licencia, basada en GNU AGPLv3 y reforzada, protege estrictamente los derechos del autor "
        "y limita el uso exclusivamente a contextos no comerciales.\n"
        "Queda terminantemente prohibido cualquier uso comercial de este software sin una licencia comercial "
        "previa, escrita y firmada por el autor.\n\n"
        "Ámbito de aplicación\n"
        "Este software comprende:\n"
        "- Código fuente y binarios.\n"
        "- Documentación, datos y scripts.\n"
        "- Interfaces gráficas y materiales visuales.\n"
        "- Derivados parciales o totales.\n\n"
        "Usos autorizados\n"
        "1. Uso personal o doméstico — exclusivo e individual.\n"
        "2. Entornos educativos, académicos o de investigación sin fines de lucro, debidamente acreditados.\n"
        "3. Organizaciones sin fines de lucro con acreditación oficial.\n\n"
        "Prohibiciones absolutas\n"
        "Sin autorización escrita del autor, está prohibido:\n"
        "- Reproducir, distribuir o sublicenciar bajo otra licencia.\n"
        "- Vender, alquilar o integrar en productos o servicios de pago.\n"
        "- Realizar ingeniería inversa, descompilación o desensamblado.\n"
        "- Entrenar o explotar modelos de IA con fines lucrativos.\n"
        "- Cualquier forma de aprovechamiento económico, directo o indirecto.\n\n"
        "Terceras bibliotecas y tecnologías\n"
        "Este producto incorpora componentes de terceros, sujetos a sus respectivas licencias:\n"
        "- pandas\n"
        "- numpy\n"
        "- tkinter\n"
        "- python‑docx\n"
        "- PyPDF2\n"
        "- python‑pptx\n"
        "- openpyxl\n"
        "- pdf2image\n"
        "- pytesseract\n\n"
        f"Titular autorizado de la licencia:\nUsuario: {usuario} | Equipo: {equipo}\n\n"
        "Denuncia por venta no autorizada:\n"
        "Si ha adquirido o le han ofrecido este software mediante venta o distribución no autorizada, "
        "denúncielo inmediatamente ante las autoridades competentes por violación de derechos de autor y fraude.\n\n"
        "Aviso legal:\n"
        "Este software está protegido por la legislación de derechos de autor y convenios internacionales. "
        "El uso no autorizado podrá acarrear sanciones civiles y penales, así como acciones legales por parte del autor."
    )
    messagebox.showinfo("Acerca de iGuanitas", texto)
