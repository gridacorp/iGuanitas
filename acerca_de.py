# acerca_de.py
import tkinter as tk
from tkinter import messagebox
import os
import webbrowser
from license import INSTALL_ID  # Importamos el ID único de instalación

def mostrar_acerca_de():
    try:
        usuario = os.getlogin()
    except Exception:
        usuario = "Usuario desconocido"
    equipo = os.environ.get('COMPUTERNAME', 'Equipo desconocido')

    texto = (
        f"Sobre iGuanitas Community v1.0\n"
        f"Copyright © 2025 José Antonio Sifuentes Maltos. Todos los derechos reservados.\n\n"
        f"Usuario: {usuario}\n"
        f"Equipo: {equipo}\n"
        f"ID de instalación (Licencia): {INSTALL_ID}\n\n"

        "Esta licencia, basada en GNU AGPLv3 y reforzada, protege estrictamente los derechos del autor "
        "y limita el uso exclusivamente a contextos no comerciales.\n"
        "Queda terminantemente prohibido cualquier uso comercial de este software sin una licencia comercial "
        "previa, escrita y firmada por el autor.\n\n"

        "Ámbito de aplicación:\n"
        "- Código fuente y binarios.\n"
        "- Documentación, datos y scripts.\n"
        "- Interfaces gráficas y materiales visuales.\n"
        "- Derivados parciales o totales.\n\n"

        "Usos autorizados:\n"
        "1. Uso personal o doméstico—exclusivo e individual.\n"
        "2. Entornos educativos, académicos o de investigación sin fines de lucro, debidamente acreditados.\n"
        "3. Organizaciones sin fines de lucro con acreditación oficial.\n\n"

        "Prohibiciones absolutas:\n"
        "- Reproducir, distribuir o sublicenciar bajo otra licencia.\n"
        "- Vender, alquilar o integrar en productos o servicios de pago.\n"
        "- Realizar ingeniería inversa, descompilación o desensamblado.\n"
        "- Entrenar o explotar modelos de IA con fines lucrativos.\n"
        "- Cualquier forma de aprovechamiento económico, directo o indirecto.\n\n"

        "Denuncia por venta no autorizada:\n"
        "Si ha adquirido o le han ofrecido este software de forma no autorizada, denúncielo ante las autoridades competentes.\n\n"

        "Aviso legal:\n"
        "Este software está protegido por la legislación de derechos de autor y convenios internacionales. "
        "El uso no autorizado podrá acarrear sanciones civiles y penales y acciones legales por parte del autor.\n\n"

        "¿Te ayudó iGuanitas?\n"
        "Apoya su desarrollo con una donación. Tu gesto mantiene vivo este proyecto. ¡Gracias!"
    )

    # Crear ventana personalizada
    ventana = tk.Toplevel()
    ventana.title("Acerca de iGuanitas Community")
    ventana.geometry("600x500")
    ventana.resizable(False, False)

    texto_widget = tk.Text(ventana, wrap="word", padx=10, pady=10)
    texto_widget.insert("1.0", texto)
    texto_widget.config(state="disabled")
    texto_widget.pack(expand=True, fill="both")

    def abrir_link():
        webbrowser.open("https://www.paypal.com/donate/?hosted_button_id=KQZ5A7HXTULZL")

    boton_donar = tk.Button(ventana, text="Donar en PayPal", command=abrir_link, bg="#0070BA", fg="white", padx=10, pady=5)
    boton_donar.pack(pady=10)

# Código para probar la ventana si ejecutas este archivo directamente:
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    mostrar_acerca_de()
    root.mainloop()
