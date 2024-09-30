import tkinter as tk
from tkinter import ttk
from conexion import conectar_db
from navegacion import cambiar_pantalla

def obtener_mayores():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT c."Cuenta_Id", c."Cuenta_Nom", t."Tran_Fecha", t."Tran_MontoDeb", t."Tran_MontoCre"
        FROM transacciones t
        JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
        ORDER BY c."Cuenta_Nom", t."Tran_Fecha"
    """)
    mayores = cur.fetchall()
    cur.close()
    conn.close()
    return mayores


def mostrar_mayores(root,reg_id):
    mayores = obtener_mayores()

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

    # Crear un canvas con scrollbar
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Mostrar cada cuenta
    for cuenta, movimientos in cuentas.items():
        frame_cuenta = ttk.Frame(scrollable_frame, relief="raised", borderwidth=1)
        frame_cuenta.pack(pady=10, padx=10, fill="x")

        for i in mayores:
            if i[0] == cuenta:
                nomcuenta = str(i[0]) + " - " + i[1]
                break

        ttk.Label(frame_cuenta, text=nomcuenta, font=("Arial", 12, "bold")).pack()

        # Crear la tabla de movimientos
        tabla = ttk.Treeview(frame_cuenta, columns=("Fecha", "Debe", "Haber"), show="headings")
        tabla.heading("Fecha", text="Fecha")
        tabla.heading("Debe", text="Debe")
        tabla.heading("Haber", text="Haber")

        saldo = 0
        for fecha, debe, haber in movimientos:
            tabla.insert("", "end", values=(fecha.strftime("%d/%m/%Y"), f"{debe:.2f}", f"{haber:.2f}"))
            saldo += debe - haber

        tabla.pack(fill="x")

        ttk.Label(frame_cuenta, text=f"Saldo Final: {saldo:.2f}", font=("Arial", 10, "bold")).pack(anchor="e")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Botón para regresar
    btn_guardar = tk.Button(root, text="Regresar", command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r))
    btn_guardar.pack(pady=10)
