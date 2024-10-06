import tkinter as tk
from tkinter import ttk
from conexion import conectar_db
from navegacion import cambiar_pantalla

def mostrar_situacion_financiera(root, reg_id):

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

    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(""" 
        SELECT "Reg_Nombre"
        FROM registros
        WHERE "Reg_Id" = %s        
    """, (reg_id,))  
    nombre_entidad = cur.fetchall()
    cur.close()
    conn.close()

    # Agregar el título
    ttk.Label(scrollable_frame, text=f"Estados financieros de {nombre_entidad}", font=("Arial", 16, "bold")).pack(pady=10)

    def update_financial_data():

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
			JOIN registros r ON r."Reg_Id" = t."Tran_RegId"
            WHERE r."Reg_Id" = %s AND c."Cuenta_CuentaTipoId" IN (1,2,3)
            GROUP BY c."Cuenta_CuentaTipoId", c."Cuenta_Id", c."Cuenta_Nom"
            ORDER BY c."Cuenta_Id", c."Cuenta_Nom"
        """, (reg_id,))  
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
			JOIN registros r ON r."Reg_Id" = t."Tran_RegId"
            WHERE r."Reg_Id" = %s AND c."Cuenta_CuentaTipoId" IN (1,2,3)
        """, (reg_id,))  
        total_activo = cur.fetchall()
        cur.close()
        conn.close()

        # Limpiar la tabla de activos y pasivos
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Crear un frame para organizar en 2 columnas (1 para activos, 1 para pasivos/patrimonio)
        container_frame = ttk.Frame(scrollable_frame)
        container_frame.pack(pady=10, padx=10, fill="x")

        # Frame para Activos (Columna izquierda)
        frame_activo = ttk.Frame(container_frame, relief="raised", borderwidth=1)
        frame_activo.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", rowspan=2)
        ttk.Label(frame_activo, text="Activos", font=("Arial", 12, "bold")).pack()

        tabla_activos = ttk.Treeview(frame_activo, columns=("Tipo", "Nota", "Nombre", "Monto"), show="headings")
        tabla_activos.heading("Tipo", text="Tipo")
        tabla_activos.heading("Nota", text="Nota")
        tabla_activos.heading("Nombre", text="Nombre")
        tabla_activos.heading("Monto", text="Monto")

        # Ajustar los anchos de las columnas
        tabla_activos.column("Tipo", width=130, stretch=False)
        tabla_activos.column("Nota", width=35, stretch=False)
        tabla_activos.column("Nombre", width=200)
        tabla_activos.column("Monto", width=100, stretch=False)

        for macho in activos:
            tabla_activos.insert("", "end", values=macho)

        tabla_activos.pack(fill="both", expand=True)
        ttk.Label(frame_activo, text=f"Activo total: {total_activo[0][0]:.2f}", font=("Arial", 10, "bold")).pack(anchor="e")

        # Consulta de Pasivos
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute(""" 
            SELECT 
                c."Cuenta_Id", 
                c."Cuenta_Nom", 
                -SUM(t."Tran_MontoDeb") + SUM(t."Tran_MontoCre") AS Monto
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
			JOIN registros r ON r."Reg_Id" = t."Tran_RegId"
            WHERE r."Reg_Id" = %s AND c."Cuenta_CuentaTipoId" = 4
            GROUP BY c."Cuenta_Id", c."Cuenta_Nom"
        """, (reg_id,)) 
        pasivos = cur.fetchall()
        cur.close()
        conn.close()

        # Total Pasivos
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute(""" 
            SELECT -SUM(t."Tran_MontoDeb") + SUM(t."Tran_MontoCre") AS Monto_total
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
			JOIN registros r ON r."Reg_Id" = t."Tran_RegId"
            WHERE r."Reg_Id" = %s AND c."Cuenta_CuentaTipoId" = 4
        """, (reg_id,))  
        total_pasivos = cur.fetchall()
        cur.close()
        conn.close()

        # Frame para Pasivos (Columna derecha arriba)
        frame_pasivos = ttk.Frame(container_frame, relief="raised", borderwidth=1)
        frame_pasivos.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ttk.Label(frame_pasivos, text="Pasivos", font=("Arial", 12, "bold")).pack()

        tabla_pasivos = ttk.Treeview(frame_pasivos, columns=("Nota", "Nombre", "Monto"), show="headings")
        tabla_pasivos.heading("Nota", text="Nota")
        tabla_pasivos.heading("Nombre", text="Nombre")
        tabla_pasivos.heading("Monto", text="Monto")

        # Ajustar los anchos de las columnas
        tabla_pasivos.column("Nota", width=35, stretch=False)
        tabla_pasivos.column("Nombre", width=200)
        tabla_pasivos.column("Monto", width=100, stretch=False) 

        for hombre in pasivos:
            tabla_pasivos.insert("", "end", values=hombre)

        tabla_pasivos.pack(fill="x")
        ttk.Label(frame_pasivos, text=f"Pasivo total: {total_pasivos[0][0]:.2f}", font=("Arial", 10, "bold")).pack(anchor="e")

        # Consulta de patrimonio
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute(""" 
            SELECT 
                c."Cuenta_Id", 
                c."Cuenta_Nom", 
                -SUM(t."Tran_MontoDeb") + SUM(t."Tran_MontoCre") AS Monto
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
			JOIN registros r ON r."Reg_Id" = t."Tran_RegId"
            WHERE r."Reg_Id" = %s AND c."Cuenta_CuentaTipoId" = 5
            GROUP BY c."Cuenta_Id", c."Cuenta_Nom"
        """, (reg_id,)) 
        patrimonio = cur.fetchall()
        cur.close()
        conn.close()

        # Total patrimonio
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute(""" 
            SELECT -SUM(t."Tran_MontoDeb") + SUM(t."Tran_MontoCre") AS Monto_total
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
			JOIN registros r ON r."Reg_Id" = t."Tran_RegId"
            WHERE r."Reg_Id" = %s AND c."Cuenta_CuentaTipoId" = 5
        """, (reg_id,))  
        total_patrimonio = cur.fetchall()
        cur.close()
        conn.close()

        # Frame para patrimonio (Columna derecha abajo)
        frame_patrimonio = ttk.Frame(container_frame, relief="raised", borderwidth=1)
        frame_patrimonio.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        ttk.Label(frame_patrimonio, text="Patrimonio", font=("Arial", 12, "bold")).pack()

        tabla_patrimonio = ttk.Treeview(frame_patrimonio, columns=("Nota", "Nombre", "Monto"), show="headings")
        tabla_patrimonio.heading("Nota", text="Nota")
        tabla_patrimonio.heading("Nombre", text="Nombre")
        tabla_patrimonio.heading("Monto", text="Monto")

        # Ajustar los anchos de las columnas
        tabla_patrimonio.column("Nota", width=35, stretch=False)
        tabla_patrimonio.column("Nombre", width=200)
        tabla_patrimonio.column("Monto", width=100, stretch=False) 

        for hombre in patrimonio:
            tabla_patrimonio.insert("", "end", values=hombre)

        tabla_patrimonio.pack(fill="x")
        ttk.Label(frame_patrimonio, text=f"Patrimonio total: {total_patrimonio[0][0]:.2f}", font=("Arial", 10, "bold")).pack(anchor="e")


    # Empaquetar canvas y scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Botón para regresar
    btn_guardar = tk.Button(root, text="Regresar", command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r))
    btn_guardar.pack(pady=10)

    # Actualizar datos por primera vez
    update_financial_data()
