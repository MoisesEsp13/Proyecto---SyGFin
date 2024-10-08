import tkinter as tk
import datetime, locale
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
        datos = []
        datos.append(cuenta)
        for i in mayores:
            if i[0] == cuenta:
                datos.append(i[1])
                break
        saldo = 0
        for i in movimientos:
            saldo += i[1] - i[2]
        datos.append(saldo)
        cuentas_neto.append(datos)


    # Labels de Título
    titulo = tk.Label(root, text="Balanza de Comprobación", font=("Helvetica", 16, "bold"))
    titulo.grid(row=0, column=1)

    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    aviso = tk.Label(root, text="Balanza a la fecha:", font=("Helvetica", 12, "bold"))
    aviso.grid(row=1, column=1)

    fecha = tk.Label(root, text=datetime.date.today().strftime("%d de %B de %Y"), font=("Helvetica", 12, "bold"))
    fecha.grid(row=2, column=1)

    # Tabla de Balanza
    columnas = ("N", "Titulo", "Debe", "Haber")
    tabla = ttk.Treeview(root, columns=columnas, show="headings")
    tabla.grid(row=3, column=1, sticky="nsew")

    # Configurar Contenido de cabeceras
    tabla.heading("N", text="")
    tabla.heading("Titulo", text="Título")
    tabla.heading("Debe", text="Debe")
    tabla.heading("Haber", text="Haber")

    # Configurar formato de cabeceras
    tabla.column("N", anchor="center", width=5, )
    tabla.column("Debe", anchor="center", width=10)
    tabla.column("Haber", anchor="center", width=10)

    # Insertar datos de la tabla
    for fila in cuentas_neto:
        if fila[2] < 0:
            tabla.insert("", "end", values=(fila[0], fila[1], "", fila[2]*(-1)))
        else:
            tabla.insert("", "end", values=(fila[0], fila[1], fila[2], ""))

    # Formato
    col1 = tk.Label(root, width=5, height=5)
    col1.grid(row=4, column=0)
    col2 = tk.Label(root, width=5, height=5)
    col2.grid(row=4, column=2)

    # Formateando el Root
    root.grid_columnconfigure(1, weight=1)

    # Botón para regresar
    btn_regresar = tk.Button(root, text="Regresar", command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r))
    btn_regresar.grid(row=4, column=1, sticky="e")