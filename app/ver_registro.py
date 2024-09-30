import tkinter as tk
from tkinter import ttk
from navegacion import cambiar_pantalla
from conexion import conectar_db

def obtener_transacciones(reg_id):
    conn = conectar_db()
    cursor = conn.cursor()
    query = '''SELECT t."Tran_Fecha", c."Cuenta_Nom", t."Tran_MontoDeb", t."Tran_MontoCre"
               FROM transacciones t
               JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
               WHERE t."Tran_RegId" = %s'''
    cursor.execute(query, (reg_id,))
    transacciones = cursor.fetchall()
    conn.close()
    return transacciones


def mostrar_ver_registro(root, reg_id):
    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()

    # Título
    titulo = tk.Label(root, text=f"Transacciones del Registro {reg_id}", font=("Helvetica", 16))
    titulo.pack(pady=10)

    # Tabla de transacciones
    transacciones = obtener_transacciones(reg_id)
    tabla = ttk.Treeview(root, columns=("Fecha", "Cuenta", "Debe", "Haber"), show="headings")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Cuenta", text="Cuenta")
    tabla.heading("Debe", text="Debe")
    tabla.heading("Haber", text="Haber")

    for trans in transacciones:
        tabla.insert("", "end", values=trans)

    tabla.pack(pady=10)

    # Botones
    btn_mayores = tk.Button(root, text="Mostrar Mayores", command=lambda: cambiar_pantalla(root, 'mayores', reg_id))
    btn_mayores.pack(side=tk.LEFT, padx=10)

    btn_situacion_financiera = tk.Button(root, text="Mostrar Estados Financieros",
                                         command=lambda: cambiar_pantalla(root, 'situacion_financiera', reg_id))
    btn_situacion_financiera.pack(side=tk.LEFT, padx=10)

    # Botón para regresar
    btn_regresar = tk.Button(root, text="Regresar", command=lambda: cambiar_pantalla(root, 'bienvenida'))
    btn_regresar.pack(side=tk.LEFT, padx=10)

