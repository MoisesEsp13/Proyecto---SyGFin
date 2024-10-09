import customtkinter as ctk
import tkinter as tk
import datetime
import locale
from tkinter import ttk
from navegacion import cambiar_pantalla
from mayores import obtener_mayores

def generar_balanza(root, reg_id):
    mayores = obtener_mayores(reg_id)

    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()

    # Agrupar por cuenta
    cuentas = {}
    for mayor in mayores:
        cuenta = mayor[0]
        if cuenta not in cuentas:
            cuentas[cuenta] = []
        cuentas[cuenta].append(mayor[2:])

    # Calcular saldo de cuentas
    cuentas_neto = []
    for cuenta, movimientos in cuentas.items():
        datos = [cuenta]
        for i in mayores:
            if i[0] == cuenta:
                datos.append(i[1])  # Nombre de la cuenta
                break
        saldo = sum(movimiento[1] - movimiento[2] for movimiento in movimientos)
        datos.append(saldo)
        cuentas_neto.append(datos)

    # Etiquetas de título
    titulo = ctk.CTkLabel(root, text="Balanza de Comprobación", font=("Helvetica", 20, "bold"), text_color="#2B6CB0")
    titulo.grid(row=0, column=1, pady=(10, 0))
    
    # Tabla de Balanza
    columnas = ("N", "Titulo", "Debe", "Haber")
    tabla = ttk.Treeview(root, columns=columnas, show="headings", height=10)
    tabla.grid(row=3, column=1, sticky="nsew", padx=20, pady=10)

    # Configurar contenido de cabeceras
    tabla.heading("N", text="Cuenta")
    tabla.heading("Titulo", text="Título")
    tabla.heading("Debe", text="Debe")
    tabla.heading("Haber", text="Haber")

    # Configurar formato de columnas
    tabla.column("N", anchor="center", width=50)
    tabla.column("Titulo", anchor="w", width=200)
    tabla.column("Debe", anchor="center", width=100)
    tabla.column("Haber", anchor="center", width=100)

    # Insertar datos en la tabla
    for fila in cuentas_neto:
        if fila[2] < 0:
            tabla.insert("", "end", values=(fila[0], fila[1], "", f"{abs(fila[2]):.2f}"))
        else:
            tabla.insert("", "end", values=(fila[0], fila[1], f"{fila[2]:.2f}", ""))

    # Configuración de diseño
    root.grid_columnconfigure(1, weight=1)

    # Botón de regreso
    btn_regresar = ctk.CTkButton(root, text="Regresar", 
                                command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r), 
                                font=("Helvetica", 16), fg_color="#4A5568", hover_color="#2D3748")
    btn_regresar.grid(row=4, column=1, padx=10, pady=10, sticky="e")
