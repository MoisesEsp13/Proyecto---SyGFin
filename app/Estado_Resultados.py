import psycopg2
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
    tk.Label(root, text="Estado de Resultados - Periodo", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2)

    tk.Label(root, text="Ventas Netas:").grid(row=1, column=0, sticky='e')
    tk.Entry(root, textvariable=ventas_netas, state="readonly").grid(row=1, column=1, padx=5, pady=5)

    tk.Label(root, text="Costo de la Venta:").grid(row=2, column=0, sticky='e')
    tk.Entry(root, textvariable=costo_ventas, state="readonly").grid(row=2, column=1, padx=5, pady=5)

    tk.Label(root, text="Utilidad Bruta:").grid(row=3, column=0, sticky='e')
    tk.Entry(root, textvariable=utilidad_bruta, state="readonly").grid(row=3, column=1, padx=5, pady=5)

    tk.Label(root, text="Gastos Operativos:").grid(row=4, column=0, sticky='e')
    tk.Entry(root, textvariable=gastos_operativos, state="readonly").grid(row=4, column=1, padx=5, pady=5)

    tk.Label(root, text="Utilidad Operativa:").grid(row=5, column=0, sticky='e')
    tk.Entry(root, textvariable=utilidad_operativa, state="readonly").grid(row=5, column=1, padx=5, pady=5)

    tk.Label(root, text="Otros Gastos:").grid(row=6, column=0, sticky='e')
    tk.Entry(root, textvariable=otros_gastos, state="readonly").grid(row=6, column=1, padx=5, pady=5)

    tk.Label(root, text="Otros Ingresos:").grid(row=7, column=0, sticky='e')
    tk.Entry(root, textvariable=otros_ingresos, state="readonly").grid(row=7, column=1, padx=5, pady=5)

    tk.Label(root, text="Utilidad Antes de Impuestos:").grid(row=8, column=0, sticky='e')
    tk.Entry(root, textvariable=utilidad_antes_impuestos, state="readonly").grid(row=8, column=1, padx=5, pady=5)

    # Botón para regresar
    btn_guardar = tk.Button(root, text="Regresar", command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r))
    btn_guardar.grid(row=9, column=0, columnspan=2, pady=10)

    # Cargar los datos del estado de resultados automáticamente al abrir la pantalla
    obtener_datos_estado_resultados(ventas_netas, costo_ventas, utilidad_bruta, gastos_operativos, utilidad_operativa, otros_gastos, otros_ingresos, utilidad_antes_impuestos)
