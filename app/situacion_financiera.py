import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from conexion import conectar_db
from navegacion import cambiar_pantalla

def mostrar_situacion_financiera(root, reg_id):

    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un canvas con scrollbar
    canvas = ctk.CTkCanvas(root, bg="#242424")
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
    ttk.Label(scrollable_frame, text=f"Estados financieros de {nombre_entidad[0][0]}", font=("Arial", 16, "bold")).pack(pady=5)

    def update_financial_data():

        # Consulta de Activos Corrientes
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute(""" 
            SELECT 
                c."Cuenta_Id", 
                c."Cuenta_Nom", 
                SUM(t."Tran_MontoDeb") - SUM(t."Tran_MontoCre") AS Monto
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
			JOIN registros r ON r."Reg_Id" = t."Tran_RegId"
            WHERE r."Reg_Id" = %s AND c."Cuenta_CuentaTipoId" IN (1,2)
            GROUP BY c."Cuenta_CuentaTipoId", c."Cuenta_Id", c."Cuenta_Nom"
            HAVING NOT SUM(t."Tran_MontoDeb") - SUM(t."Tran_MontoCre")=0
            ORDER BY c."Cuenta_Id", c."Cuenta_Nom"
        """, (reg_id,))  
        activos_corrientes = cur.fetchall()
        cur.close()
        conn.close()

        # Consulta de Activos NO Corrientes
        conn = conectar_db()
        cur = conn.cursor()
        cur.execute(""" 
            SELECT 
                c."Cuenta_Id", 
                c."Cuenta_Nom", 
                SUM(t."Tran_MontoDeb") - SUM(t."Tran_MontoCre") AS Monto
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
			JOIN registros r ON r."Reg_Id" = t."Tran_RegId"
            WHERE r."Reg_Id" = %s AND c."Cuenta_CuentaTipoId" = 3
            GROUP BY c."Cuenta_CuentaTipoId", c."Cuenta_Id", c."Cuenta_Nom"
            HAVING NOT SUM(t."Tran_MontoDeb") - SUM(t."Tran_MontoCre")=0        
            ORDER BY c."Cuenta_Id", c."Cuenta_Nom"
        """, (reg_id,))  
        activos_no_corrientes = cur.fetchall()
        cur.close()
        conn.close()

        # Total de Activos Corrientes y No Corrientes
        total_activos_corrientes = sum(monto[2] for monto in activos_corrientes)
        total_activos_no_corrientes = sum(monto[2] for monto in activos_no_corrientes)
        total_activos = total_activos_corrientes + total_activos_no_corrientes
       
        # Limpiar la tabla de activos y pasivos
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Crear un frame para organizar en 2 columnas (1 para activos, 1 para pasivos/patrimonio)
        container_frame = ttk.Frame(scrollable_frame)
        container_frame.pack(pady=5, padx=10, fill="x")

        #Nombre
        frame_titulo = ttk.Frame(container_frame, relief="raised", borderwidth=1)
        frame_titulo.grid(row=0, column=0, padx=10, pady=5, sticky="nsew", columnspan=2)
        ttk.Label(frame_titulo, text=f"Estados financieros de {nombre_entidad[0][0]}", font=("Arial", 16, "bold")).pack()

        # Frame para Activos (Columna izquierda)
        frame_activos_corrientes = ttk.Frame(container_frame, relief="raised", borderwidth=1, height=50)
        frame_activos_corrientes.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        ttk.Label(frame_activos_corrientes, text="Activos Corrientes", font=("Arial", 12, "bold")).pack()

        tabla_activos_corrientes = ttk.Treeview(frame_activos_corrientes, columns=("Nota", "Nombre", "Monto"), show="headings")
        tabla_activos_corrientes.heading("Nota", text="Nota")
        tabla_activos_corrientes.heading("Nombre", text="Nombre")
        tabla_activos_corrientes.heading("Monto", text="Monto")

        # Ajustar los anchos de las columnas
        tabla_activos_corrientes.column("Nota", width=35, stretch=False)
        tabla_activos_corrientes.column("Nombre", width=230)
        tabla_activos_corrientes.column("Monto", width=100, stretch=False)

        for activo in activos_corrientes:
            tabla_activos_corrientes.insert("", "end", values=activo)

        tabla_activos_corrientes.pack(fill="both", expand=True)
        ttk.Label(frame_activos_corrientes, text=f"Total de Activos Corrientes: {total_activos_corrientes:.2f}", font=("Arial", 10, "bold")).pack(anchor="e")

        # Frame para Activos_no_corrientes (Columna izquierda)
        frame_activos_no_corrientes = ttk.Frame(container_frame, relief="raised", borderwidth=1, height=50)
        frame_activos_no_corrientes.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        ttk.Label(frame_activos_no_corrientes, text="Activos No Corrientes", font=("Arial", 12, "bold")).pack()

        tabla_activos_no_corrientes = ttk.Treeview(frame_activos_no_corrientes, columns=("Nota", "Nombre", "Monto"), show="headings")
        tabla_activos_no_corrientes.heading("Nota", text="Nota")
        tabla_activos_no_corrientes.heading("Nombre", text="Nombre")
        tabla_activos_no_corrientes.heading("Monto", text="Monto")

        # Ajustar los anchos de las columnas
        tabla_activos_no_corrientes.column("Nota", width=35, stretch=False)
        tabla_activos_no_corrientes.column("Nombre", width=230)
        tabla_activos_no_corrientes.column("Monto", width=100, stretch=False)

        for activo in activos_no_corrientes:
            tabla_activos_no_corrientes.insert("", "end", values=activo)

        tabla_activos_no_corrientes.pack(fill="both", expand=True)
        ttk.Label(frame_activos_no_corrientes, text=f"Activo total: {total_activos_no_corrientes:.2f}", font=("Arial", 10, "bold")).pack(anchor="e")

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
            HAVING NOT SUM(t."Tran_MontoDeb") - SUM(t."Tran_MontoCre")=0
        """, (reg_id,)) 
        pasivos = cur.fetchall()
        cur.close()
        conn.close()

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
            HAVING NOT SUM(t."Tran_MontoDeb") - SUM(t."Tran_MontoCre")=0
        """, (reg_id,)) 
        patrimonio = cur.fetchall()
        cur.close()
        conn.close()

        conn = conectar_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                SUM(CASE WHEN c."Cuenta_Id" = 70 THEN t."Tran_MontoCre" ELSE 0 END) AS "VentasNetas",
                SUM(CASE WHEN c."Cuenta_Id" IN (69, 61, 68) THEN t."Tran_MontoDeb" ELSE 0 END) AS "CostoVenta",
                SUM(CASE WHEN c."Cuenta_Id" IN (95, 62, 63, 64, 94) THEN t."Tran_MontoDeb" ELSE 0 END) AS "GastosOperativos",
                SUM(CASE WHEN c."Cuenta_Id" = 67 THEN t."Tran_MontoDeb" ELSE 0 END) AS "GastosFinancieros",
                SUM(CASE WHEN c."Cuenta_Id" IN (75, 73, 77) THEN t."Tran_MontoCre" ELSE 0 END) AS "OtrosIngresos",
                SUM(CASE WHEN c."Cuenta_Id" IN (65, 66) THEN t."Tran_MontoDeb" ELSE 0 END) AS "OtrosGastos"
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id";
        """)

        # Código para obtener las cifras del estado de resultados
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                SUM(CASE WHEN c."Cuenta_Id" = 70 THEN t."Tran_MontoCre" ELSE 0 END) AS "VentasNetas",
                SUM(CASE WHEN c."Cuenta_Id" IN (69, 61, 68) THEN t."Tran_MontoDeb" ELSE 0 END) AS "CostoVenta",
                SUM(CASE WHEN c."Cuenta_Id" IN (95, 62, 63, 64, 94) THEN t."Tran_MontoDeb" ELSE 0 END) AS "GastosOperativos",
                SUM(CASE WHEN c."Cuenta_Id" = 67 THEN t."Tran_MontoDeb" ELSE 0 END) AS "GastosFinancieros",
                SUM(CASE WHEN c."Cuenta_Id" IN (75, 73, 77) THEN t."Tran_MontoCre" ELSE 0 END) AS "OtrosIngresos",
                SUM(CASE WHEN c."Cuenta_Id" IN (65, 66) THEN t."Tran_MontoDeb" ELSE 0 END) AS "OtrosGastos"
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id";
        """)

        resultado = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        # Verificar y asignar valores
        ventas_netas_valor = resultado[0] if len(resultado) > 0 and resultado[0] is not None else 0
        costo_ventas_valor = resultado[1] if len(resultado) > 1 and resultado[1] is not None else 0
        gastos_operativos_valor = resultado[2] if len(resultado) > 2 and resultado[2] is not None else 0
        gastos_financieros_valor = resultado[3] if len(resultado) > 3 and resultado[3] is not None else 0
        otros_ingresos_valor = resultado[4] if len(resultado) > 4 and resultado[4] is not None else 0
        otros_gastos_valor = resultado[5] if len(resultado) > 5 and resultado[5] is not None else 0

        # Asignar valores a los campos correspondientes
        utilidad_antes_impuestos_valor = ventas_netas_valor - costo_ventas_valor - gastos_operativos_valor - gastos_financieros_valor + otros_ingresos_valor - otros_gastos_valor
        patrimonio.append(("-", "Utilidad acumulada", utilidad_antes_impuestos_valor))

        # Total pasivos y patrimonio
        total_pasivos = sum(monto[2] for monto in pasivos)
        total_patrimonio = sum(monto[2] for monto in patrimonio)
        total_pasivos_y_patrimonio = total_pasivos + total_patrimonio

        # Frame para Pasivos (Columna derecha arriba)
        frame_pasivos = ttk.Frame(container_frame, relief="raised", borderwidth=1, height=50)
        frame_pasivos.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
        ttk.Label(frame_pasivos, text="Pasivos", font=("Arial", 12, "bold")).pack()

        tabla_pasivos = ttk.Treeview(frame_pasivos, columns=("Nota", "Nombre", "Monto"), show="headings")
        tabla_pasivos.heading("Nota", text="Nota")
        tabla_pasivos.heading("Nombre", text="Nombre")
        tabla_pasivos.heading("Monto", text="Monto")

        # Ajustar los anchos de las columnas
        tabla_pasivos.column("Nota", width=35, stretch=False)
        tabla_pasivos.column("Nombre", width=230)
        tabla_pasivos.column("Monto", width=100, stretch=False) 

        for pas in pasivos:
            tabla_pasivos.insert("", "end", values=pas)

        tabla_pasivos.pack(fill="x")
        ttk.Label(frame_pasivos, text=f"Pasivo total: {total_pasivos:.2f}", font=("Arial", 10, "bold")).pack(anchor="e")

        # Frame para patrimonio (Columna derecha abajo)
        frame_patrimonio = ttk.Frame(container_frame, relief="raised", borderwidth=1, height=50)
        frame_patrimonio.grid(row=2, column=1, padx=10, pady=5, sticky="nsew")
        ttk.Label(frame_patrimonio, text="Patrimonio", font=("Arial", 12, "bold")).pack()

        tabla_patrimonio = ttk.Treeview(frame_patrimonio, columns=("Nota", "Nombre", "Monto"), show="headings")
        tabla_patrimonio.heading("Nota", text="Nota")
        tabla_patrimonio.heading("Nombre", text="Nombre")
        tabla_patrimonio.heading("Monto", text="Monto")

        # Ajustar los anchos de las columnas
        tabla_patrimonio.column("Nota", width=35, stretch=False)
        tabla_patrimonio.column("Nombre", width=230)
        tabla_patrimonio.column("Monto", width=100, stretch=False) 

        for patr in patrimonio:
            tabla_patrimonio.insert("", "end", values=patr)

        tabla_patrimonio.pack(fill="x")
        ttk.Label(frame_patrimonio, text=f"Patrimonio total: {total_patrimonio:.2f}", font=("Arial", 10, "bold")).pack(anchor="e")

        #Para ver el total
        frame_activos = ttk.Frame(container_frame, relief="raised", borderwidth=1)
        frame_activos.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        ttk.Label(frame_activos, text=f"Total Activos: {total_activos:.2f}", font=("Arial", 12, "bold")).pack()

        frame_pas_patr = ttk.Frame(container_frame, relief="raised", borderwidth=1)
        frame_pas_patr.grid(row=3, column=1, padx=10, pady=5, sticky="nsew")
        ttk.Label(frame_pas_patr, text=f"Total Pasivos y Patrimonio: {total_pasivos_y_patrimonio:.2f}", font=("Arial", 12, "bold")).pack()
 
    # Empaquetar canvas y scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Botón para regresar
    btn_guardar = ctk.CTkButton(root, text="Regresar", 
                                command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r), 
                                font=("Helvetica", 16), fg_color="#4A5568", hover_color="#2D3748")
    btn_guardar.pack(pady=10)

    # Actualizar datos por primera vez
    update_financial_data()
