import customtkinter as ctk
import tkinter as tk
import random
from tkinter import ttk
from conexion import conectar_db
from navegacion import cambiar_pantalla

def obtener_mayores(reg_id):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT c."Cuenta_Id", c."Cuenta_Nom", t."Tran_Fecha", t."Tran_MontoDeb", t."Tran_MontoCre"
        FROM transacciones t
        JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
        WHERE t."Tran_RegId" = %s
        ORDER BY c."Cuenta_Nom", t."Tran_Fecha"
    """, (reg_id,))
    mayores = cur.fetchall()
    cur.close()
    conn.close()
    return mayores

def color():
    colores_predefinidos = [
    "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige",
    "bisque", "blanchedalmond", "blue", "cornflowerblue", "cornsilk", 
    "cyan", "darkorange", "floralwhite", "fuchsia", "gainsboro", 
    "ghostwhite", "gold", "goldenrod", "gray", "green", 
    "greenyellow", "honeydew", "hotpink", "ivory", "khaki", 
    "lavender", "lavenderblush", "lawngreen", "lemonchiffon", "lightblue",
    "lightcoral", "lightcyan", "lightgoldenrodyellow", "lightgray", 
    "lightgreen", "lightpink", "lightsalmon", "lightyellow", 
    "magenta", "mediumaquamarine", "mediumblue", "mediumorchid",
    "mediumpurple", "mediumseagreen", "mediumslateblue", "mediumturquoise",
    "mediumvioletred", "mintcream", "mistyrose", "moccasin", 
    "navajowhite", "oldlace", "olive", "orange", "orangered", 
    "orchid", "palegoldenrod", "palegreen", "paleturquoise", 
    "palevioletred", "papayawhip", "peachpuff", "pink", 
    "plum", "powderblue", "rosybrown", "royalblue", "sandybrown", 
    "seashell", "silver", "skyblue", "slategray", "snow", 
    "springgreen", "tan", "thistle", "tomato", "turquoise", 
    "violet", "wheat", "white", "whitesmoke", "yellow", 
    "yellowgreen"]
    return random.choice(colores_predefinidos)


def mostrar_mayores(root, reg_id):
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

    # Crear un canvas
    canvas = ctk.CTkCanvas(root, bg="#242424")
    canvas.grid(row=1, column=0, sticky="nsew")

    # Crear una barra de desplazamiento para el canvas
    scrollbar = ctk.CTkScrollbar(root, orientation="vertical", command=canvas.yview)
    scrollbar.grid(row=1, column=1, sticky="ns")

    # Configurar el canvas para funcionar con la barra de desplazamiento
    canvas.configure(yscrollcommand=scrollbar.set)

    # Crear un Frame dentro del canvas
    scrollable_frame = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Formateando el root
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Definir estilo para tablas con fondo blanco
    estilo = ttk.Style()
    estilo.configure("White.Treeview", background="white", fieldbackground="white", foreground="black")

    # Contador de cuentas
    contador = 0

    # Mostrar el mayor de cada cuenta
    for cuenta, movimientos in cuentas.items():
        # Crear un Frame para cada cuenta
        frame_cuenta = ctk.CTkFrame(scrollable_frame, border_width=1, fg_color="lightgray", corner_radius=10)
        frame_cuenta.grid(row=contador, column=0, pady=10, padx=10, sticky="nsew")

        # Buscar nombre de la cuenta
        for i in mayores:
            if i[0] == cuenta:
                nomcuenta = str(i[0]) + " - " + i[1]
                break
        
        # Colocar Título
        titulo = ttk.Label(frame_cuenta, background=color(), text=nomcuenta, font=("Arial", 12, "bold"), anchor="center")
        titulo.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # Crear linea interior
        linea = tk.Label(frame_cuenta, width=1, bg="black")
        linea.grid(row=1, column=1, sticky="nsew")

        # Crear la tabla de movimientos
        columns1 = ("Fecha", "Debe")
        columns2 = ("Haber", "Fecha")
        tabla1 = ttk.Treeview(frame_cuenta, columns=columns1, show="headings", style="White.Treeview", height=5)
        tabla2 = ttk.Treeview(frame_cuenta, columns=columns2, show="headings", style="White.Treeview", height=5)

        # Definir Encabezados
        tabla1.heading("Fecha", text="Fecha")
        tabla1.heading("Debe", text="Debe")
        tabla2.heading("Haber", text="Haber")
        tabla2.heading("Fecha", text="Fecha")

        # Centrar Contenidos
        tabla1.column("Fecha", anchor="center")
        tabla1.column("Debe", anchor="center")
        tabla2.column("Haber", anchor="center")
        tabla2.column("Fecha", anchor="center")

        # Calcular saldo e insertar datos a la tabla
        saldo = 0
        for fecha, debe, haber in movimientos:
            if debe != 0:
                tabla1.insert("", "end", values=(fecha.strftime("%d/%m/%Y"), f"{debe:.2f}"))
            if haber != 0:
                tabla2.insert("", "end", values=(f"{haber:.2f}", fecha.strftime("%d/%m/%Y")))
            saldo += debe - haber

        # Ubicar Tabla
        tabla1.grid(row=1, column=0, sticky="nsew")
        tabla2.grid(row=1, column=2, sticky="nsew")
        frame_cuenta.grid_rowconfigure(0, weight=1)
        frame_cuenta.grid_columnconfigure(0, weight=1)

        # Ubicar saldos
        if saldo < 0:
            saldo = saldo * (-1)
            saldo_neto = ctk.CTkLabel(frame_cuenta, text=f"Saldo Final: {saldo:.2f}", 
                                      font=("Arial", 13, "bold"),
                                      text_color="black")
            saldo_neto.grid(row=2, column=2, padx=3, pady=3)
        else:
            saldo_neto = ctk.CTkLabel(frame_cuenta, text=f"Saldo Final: {saldo:.2f}", 
                                      font=("Arial", 13, "bold"),
                                      text_color="black")
            saldo_neto.grid(row=2, column=0, padx=3, pady=3)
        
        contador += 1

    # Ajustar la región del canvas al contenido
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Título Ventana
    ventana = ctk.CTkLabel(root, text="Mayores del registro", font=("Helvetica", 20, "bold"), text_color="#2B6CB0")
    ventana.grid(row=0, column=0, columnspan=2, pady=10)

    # Botón para regresar
    btn_guardar = ctk.CTkButton(root, text="Regresar", 
                                command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r), 
                                font=("Helvetica", 16), fg_color="#4A5568", hover_color="#2D3748")
    btn_guardar.grid(row=0, column=2, padx=10, pady=10, sticky="e")
