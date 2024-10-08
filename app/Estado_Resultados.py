import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from navegacion import cambiar_pantalla
from conexion import conectar_db

# Función para obtener los datos del estado de resultados
def obtener_datos_estado_resultados(ventas_netas, costo_ventas, utilidad_bruta, gastos_operativos, utilidad_operativa,
                                    otros_gastos, otros_ingresos, utilidad_antes_impuestos):
    conn = conectar_db()
    if conn is None:
        return
    
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

    # Verificar la longitud de la tupla de resultados y manejar la ausencia de columnas
    ventas_netas_valor = resultado[0] if len(resultado) > 0 and resultado[0] is not None else 0
    costo_ventas_valor = resultado[1] if len(resultado) > 1 and resultado[1] is not None else 0
    gastos_operativos_valor = resultado[2] if len(resultado) > 2 and resultado[2] is not None else 0
    gastos_financieros_valor = resultado[3] if len(resultado) > 3 and resultado[3] is not None else 0
    otros_ingresos_valor = resultado[4] if len(resultado) > 4 and resultado[4] is not None else 0
    otros_gastos_valor = resultado[5] if len(resultado) > 5 and resultado[5] is not None else 0

    # Asignar valores a los campos correspondientes
    ventas_netas.set(f"S/. {ventas_netas_valor:,.2f}")
    costo_ventas.set(f"S/. {costo_ventas_valor:,.2f}")
    utilidad_bruta.set(f"S/. {(ventas_netas_valor - costo_ventas_valor):,.2f}")
    gastos_operativos.set(f"S/. {(gastos_operativos_valor + gastos_financieros_valor):,.2f}")
    utilidad_operativa.set(f"S/. {(ventas_netas_valor - costo_ventas_valor - gastos_operativos_valor - gastos_financieros_valor):,.2f}")
    otros_ingresos.set(f"S/. {otros_ingresos_valor:,.2f}")
    otros_gastos.set(f"S/. {otros_gastos_valor:,.2f}")
    utilidad_antes_impuestos.set(f"S/. {(ventas_netas_valor - costo_ventas_valor - gastos_operativos_valor - gastos_financieros_valor + otros_ingresos_valor - otros_gastos_valor):,.2f}")

# Pantalla del estado de resultados
def abrir_estado_resultados(root, reg_id):
    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()
    
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute(""" 
        SELECT "Reg_Nombre"
        FROM registros
        WHERE "Reg_Id" = %s        
    """, (reg_id,))  
    nombre_entidad = cur.fetchone() 
    cur.close()
    conn.close()
    nombre_entidad_valor = nombre_entidad[0]

    # Variables para los campos del estado de resultados
    ventas_netas = tk.StringVar()
    costo_ventas = tk.StringVar()
    utilidad_bruta = tk.StringVar()
    gastos_operativos = tk.StringVar()
    utilidad_operativa = tk.StringVar()
    otros_gastos = tk.StringVar()
    otros_ingresos = tk.StringVar()
    utilidad_antes_impuestos = tk.StringVar()

    # Crear y organizar la interfaz gráfica
    # Encabezado centrado
    titulo = ctk.CTkLabel(root, text=f"Estado de Resultados - {nombre_entidad_valor}", font=("Helvetica", 24, "bold"), text_color="#2B6CB0")
    titulo.grid(row=0, column=0, columnspan=2, pady=20)
    
    # Ventas Netas (Resaltado)
    ctk.CTkLabel(root, text="Ventas Netas:", font=("Arial", 12, "bold"), text_color="#2B6CB0").grid(row=1, column=0, sticky="e", padx=10)
    ctk.CTkEntry(root, textvariable=ventas_netas, state="readonly").grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Costo de la Venta
    ctk.CTkLabel(root, text="Costo de la Venta:", font=("Arial", 12), text_color="#2B6CB0").grid(row=2, column=0, sticky="e", padx=10)
    ctk.CTkEntry(root, textvariable=costo_ventas, state="readonly").grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Utilidad Bruta (Resaltado)
    ctk.CTkLabel(root, text="Utilidad Bruta:", font=("Arial", 12, "bold"), text_color="#2B6CB0").grid(row=3, column=0, sticky="e", padx=10)
    ctk.CTkEntry(root, textvariable=utilidad_bruta, state="readonly").grid(row=3, column=1, padx=5, pady=5, sticky="w")

    # Gastos Operativos
    ctk.CTkLabel(root, text="Gastos Operativos:", font=("Arial", 12), text_color="#2B6CB0").grid(row=4, column=0, sticky="e", padx=10)
    ctk.CTkEntry(root, textvariable=gastos_operativos, state="readonly").grid(row=4, column=1, padx=5, pady=5, sticky="w")

    # Utilidad Operativa (Resaltado)
    ctk.CTkLabel(root, text="Utilidad Operativa:", font=("Arial", 12, "bold"), text_color="#2B6CB0").grid(row=5, column=0, sticky="e", padx=10)
    ctk.CTkEntry(root, textvariable=utilidad_operativa, state="readonly").grid(row=5, column=1, padx=5, pady=5, sticky="w")

    # Otros Gastos
    ctk.CTkLabel(root, text="Otros Gastos:", font=("Arial", 12), text_color="#2B6CB0").grid(row=6, column=0, sticky="e", padx=10)
    ctk.CTkEntry(root, textvariable=otros_gastos, state="readonly").grid(row=6, column=1, padx=5, pady=5, sticky="w")

    # Otros Ingresos
    ctk.CTkLabel(root, text="Otros Ingresos:", font=("Arial", 12), text_color="#2B6CB0").grid(row=7, column=0, sticky="e", padx=10)
    ctk.CTkEntry(root, textvariable=otros_ingresos, state="readonly").grid(row=7, column=1, padx=5, pady=5, sticky="w")

    # Utilidad Antes de Impuestos (Resaltado)
    ctk.CTkLabel(root, text="Utilidad Antes de Impuestos:", font=("Arial", 12, "bold"), text_color="#2B6CB0").grid(row=8, column=0, sticky="e", padx=10)
    ctk.CTkEntry(root, textvariable=utilidad_antes_impuestos, state="readonly").grid(row=8, column=1, padx=5, pady=5, sticky="w")

    # Botón para regresar
    btn_regresar = ctk.CTkButton(root, text="Regresar", fg_color="#4A5568", hover_color="#2D3748", text_color="white",
                                 command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r))
    btn_regresar.grid(row=9, column=0, columnspan=2, pady=20)

    # Configurar el centrado y alineación
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Cargar los datos del estado de resultados automáticamente al abrir la pantalla
    obtener_datos_estado_resultados(ventas_netas, costo_ventas, utilidad_bruta, gastos_operativos, utilidad_operativa, otros_gastos, otros_ingresos, utilidad_antes_impuestos)
