import tkinter as tk
from tkinter import ttk
from conexion import conectar_db
from navegacion import cambiar_pantalla

def obtener_anios():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(""" 
        SELECT DISTINCT EXTRACT(YEAR FROM t."Tran_Fecha")::INTEGER AS anio 
        FROM transacciones t 
        ORDER BY anio; 
    """)
    anios = cur.fetchall()
    cur.close()
    conn.close()
    return [anio[0] for anio in anios]

def obtener_transacciones(anio,tipo):
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(""" 
        SELECT c."Cuenta_CuentaTipoId", c."Cuenta_Id", c."Cuenta_Nom", 
               SUM(t."Tran_MontoDeb") + SUM(t."Tran_MontoCre") as Monto
        FROM transacciones t
        JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
        WHERE EXTRACT(YEAR FROM t."Tran_Fecha") = %s AND c."Cuenta_CuentaTipoId" = %s
        GROUP BY c."Cuenta_CuentaTipoId", c."Cuenta_Id", c."Cuenta_Nom"
        ORDER BY c."Cuenta_Id", c."Cuenta_Nom"
    """, (anio,tipo,))  # Aquí se corrige la colocación de la tupla
    transacciones = cur.fetchall()
    cur.close()
    conn.close()
    return transacciones

def mostrar_situacion_financiera(root,reg_id):
    anios = obtener_anios()

    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()
    
    # Crear un canvas con scrollbar
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    # Título
    titulo = tk.Label(root, text=f"Situacion financiera", font=("Helvetica", 16))
    titulo.pack(pady=10)

    tipos = [2,3,4,5]
    anio =2024

    # Tabla de transacciones
    for tipo in tipos:
        transacciones = obtener_transacciones(anio,tipo)
        tabla = ttk.Treeview(root, columns=("Tipo", "Nota", "Cuenta", "Monto"), show="headings")
        tabla.heading("Tipo", text="Tipo")
        tabla.heading("Nota", text="Nota")
        tabla.heading("Cuenta", text="Cuenta")
        tabla.heading("Monto", text="Monto")
        
        for trans in transacciones:
            tabla.insert("", "end", values=trans)
        tabla.pack(pady=10)


    # Botón para regresar
    btn_guardar = tk.Button(root, text="Regresar", command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r))
    btn_guardar.pack(pady=10)
    

