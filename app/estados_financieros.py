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

def mostrar_situacion_financiera(root, reg_id):
    anios = obtener_anios()

    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()

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

    # Combobox para seleccionar el año
    selected_year = tk.IntVar(value=anios[0])  # Inicializa con el primer año
    year_combobox = ttk.Combobox(root, textvariable=selected_year, values=anios, state="readonly")
    year_combobox.pack(pady=10)

    def update_financial_data():
        anio = selected_year.get()

        # Consulta de Activos
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute(""" 
            SELECT 
                CASE
                    WHEN c."Cuenta_CuentaTipoId" = 1 THEN 'Corriente'
                    WHEN c."Cuenta_CuentaTipoId" = 2 THEN 'Corriente (Existencias)'
                    WHEN c."Cuenta_CuentaTipoId" = 3 THEN 'No Corriente'
                END AS tipo,
                c."Cuenta_Id", 
                c."Cuenta_Nom", 
                SUM(t."Tran_MontoDeb") - SUM(t."Tran_MontoCre") AS Monto
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
            WHERE EXTRACT(YEAR FROM t."Tran_Fecha") = %s AND c."Cuenta_CuentaTipoId" IN (1,2,3)
            GROUP BY c."Cuenta_CuentaTipoId", c."Cuenta_Id", c."Cuenta_Nom"
            ORDER BY c."Cuenta_Id", c."Cuenta_Nom"
        """, (anio,))  
        activos = cur.fetchall()
        cur.close()
        conn.close()

        # Total de Activos
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute(""" 
            SELECT SUM(t."Tran_MontoDeb") - SUM(t."Tran_MontoCre") AS Monto_total
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
            WHERE EXTRACT(YEAR FROM t."Tran_Fecha") = %s AND c."Cuenta_CuentaTipoId" IN (1,2,3)
        """, (anio,))  
        total_activo = cur.fetchall()
        cur.close()
        conn.close()

        # Limpiar la tabla de activos
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Mostrar activos
        frame_activo = ttk.Frame(scrollable_frame, relief="raised", borderwidth=1)
        frame_activo.pack(pady=10, padx=10, fill="x")
        ttk.Label(frame_activo, text="Activos", font=("Arial", 12, "bold")).pack()

        tabla = ttk.Treeview(frame_activo, columns=("Tipo", "Nota", "Nombre", "Monto"), show="headings")
        tabla.heading("Tipo", text="Tipo")
        tabla.heading("Nota", text="Nota")
        tabla.heading("Nombre", text="Nombre")
        tabla.heading("Monto", text="Monto")

        for macho in activos:
            tabla.insert("", "end", values=macho)

        tabla.pack(fill="x")
        ttk.Label(frame_activo, text=f"Activo total: {total_activo[0][0]:.2f}", font=("Arial", 10, "bold")).pack(anchor="e")

        # Consulta de Pasivos y Patrimonio
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute(""" 
            SELECT 
                'Pasivo' AS tipo,
                c."Cuenta_Id", 
                c."Cuenta_Nom", 
                -SUM(t."Tran_MontoDeb") + SUM(t."Tran_MontoCre") AS Monto
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
            WHERE EXTRACT(YEAR FROM t."Tran_Fecha") = %s AND c."Cuenta_CuentaTipoId" = 4
            GROUP BY c."Cuenta_Id", c."Cuenta_Nom"

            UNION ALL

            SELECT 
                'Suma Total Pasivos' AS tipo,
                0, 
                ' ', 
                -SUM(t."Tran_MontoDeb") + SUM(t."Tran_MontoCre") AS Monto
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
            WHERE EXTRACT(YEAR FROM t."Tran_Fecha") = %s AND c."Cuenta_CuentaTipoId" = 4

            UNION ALL

            SELECT 
                'Patrimonio' AS tipo,
                c."Cuenta_Id", 
                c."Cuenta_Nom", 
                -SUM(t."Tran_MontoDeb") + SUM(t."Tran_MontoCre") AS Monto
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
            WHERE EXTRACT(YEAR FROM t."Tran_Fecha") = %s AND c."Cuenta_CuentaTipoId" = 5
            GROUP BY c."Cuenta_Id", c."Cuenta_Nom"

            UNION ALL

            SELECT 
                'Suma Total Patrimonio' AS tipo,
                0, 
                ' ', 
                -SUM(t."Tran_MontoDeb") + SUM(t."Tran_MontoCre") AS Monto
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
            WHERE EXTRACT(YEAR FROM t."Tran_Fecha") = %s AND c."Cuenta_CuentaTipoId" = 5
        """, (anio, anio, anio, anio))  
        pas_patr = cur.fetchall()
        cur.close()
        conn.close()

        # Total Pasivos y Patrimonio
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute(""" 
            SELECT -SUM(t."Tran_MontoDeb") + SUM(t."Tran_MontoCre") AS Monto_total
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
            WHERE EXTRACT(YEAR FROM t."Tran_Fecha") = %s AND c."Cuenta_CuentaTipoId" IN (4,5)
        """, (anio,))  
        total_pas_patr = cur.fetchall()
        cur.close()
        conn.close()

        # Mostrar pasivos y patrimonio
        frame_pas_patr = ttk.Frame(scrollable_frame, relief="raised", borderwidth=1)
        frame_pas_patr.pack(pady=10, padx=10, fill="x")
        ttk.Label(frame_pas_patr, text="Pasivos y Patrimonios", font=("Arial", 12, "bold")).pack()

        tabla = ttk.Treeview(frame_pas_patr, columns=("Tipo", "Nota", "Nombre", "Monto"), show="headings")
        tabla.heading("Tipo", text="Tipo")
        tabla.heading("Nota", text="Nota")
        tabla.heading("Nombre", text="Nombre")
        tabla.heading("Monto", text="Monto")

        for hombre in pas_patr:
            tabla.insert("", "end", values=hombre)

        tabla.pack(fill="x")
        ttk.Label(frame_pas_patr, text=f"Pasivo y Patrimonio total: {total_pas_patr[0][0]:.2f}", font=("Arial", 10, "bold")).pack(anchor="e")

    # Botón para actualizar datos
    btn_actualizar = tk.Button(root, text="Actualizar", command=update_financial_data)
    btn_actualizar.pack(pady=10)

    # Empaquetar canvas y scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Botón para regresar
    btn_guardar = tk.Button(root, text="Regresar", command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r))
    btn_guardar.pack(pady=10)

    # Inicializar con el primer año
    update_financial_data()
