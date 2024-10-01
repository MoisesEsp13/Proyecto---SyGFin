import psycopg2
import tkinter as tk
from tkinter import ttk
from navegacion import cambiar_pantalla

# Función para conectar a la base de datos
def conectar_db():
    try:
        conn = psycopg2.connect(dbname="SistemaContable", user="postgres",
                                password="123456", host="localhost", port="5432")
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Función para obtener los datos del estado de resultados
def obtener_datos_estado_resultados():
    conn = conectar_db()
    if conn is None:
        return
    
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            SUM(CASE WHEN c."Cuenta_Id" = 70 THEN t."Tran_MontoCre" ELSE 0 END) AS "VentasNetas",
            SUM(CASE WHEN c."Cuenta_Id" = 69 THEN t."Tran_MontoDeb" ELSE 0 END) AS "CostoVenta",
            SUM(CASE WHEN c."Cuenta_Id" = 95 THEN t."Tran_MontoDeb" ELSE 0 END) AS "GastosVenta",
            SUM(CASE WHEN c."Cuenta_Id" = 94 THEN t."Tran_MontoDeb" ELSE 0 END) AS "GastosAdmi",
            SUM(CASE WHEN c."Cuenta_Id" = 67 THEN t."Tran_MontoDeb" ELSE 0 END) AS "GastosFinancieros",
            SUM(CASE WHEN c."Cuenta_Id" = 75 THEN t."Tran_MontoCre" ELSE 0 END) AS "OtrosIngresos",
            SUM(CASE WHEN c."Cuenta_Id" = 65 THEN t."Tran_MontoDeb" ELSE 0 END) AS "OtrosGastos"
        FROM transacciones t
        JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
    """)
    
    resultado = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    # Asignar valores a los campos correspondientes
    ventas_netas.set(f"S/. {resultado[0] if resultado[0] is not None else 0:,.2f}")
    costo_ventas.set(f"S/. {resultado[1] if resultado[1] is not None else 0:,.2f}")
    utilidad_bruta.set(f"S/. {(resultado[0] if resultado[0] is not None else 0) - (resultado[1] if resultado[1] is not None else 0):,.2f}")
    gastos_operativos.set(f"S/. {(resultado[2] if resultado[2] is not None else 0) + (resultado[3] if resultado[3] is not None else 0):,.2f}")
    utilidad_operativa.set(f"S/. {(resultado[0] if resultado[0] is not None else 0) - (resultado[1] if resultado[1] is not None else 0) - (resultado[2] if resultado[2] is not None else 0) - (resultado[3] if resultado[3] is not None else 0):,.2f}")
    otros_gastos.set(f"S/. {resultado[6] if resultado[6] is not None else 0:,.2f}")
    otros_ingresos.set(f"S/. {resultado[5] if resultado[5] is not None else 0:,.2f}")
    utilidad_antes_impuestos.set(f"S/. {(resultado[0] if resultado[0] is not None else 0) - (resultado[1] if resultado[1] is not None else 0) - (resultado[2] if resultado[2] is not None else 0) - (resultado[3] if resultado[3] is not None else 0) + (resultado[5] if resultado[5] is not None else 0) - (resultado[6] if resultado[6] is not None else 0):,.2f}")
# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Estado de Resultados - Sistema Contable")
root.geometry("800x600")

# Variables para los campos del estado de resultados
ventas_netas = tk.StringVar()
costo_ventas = tk.StringVar()
utilidad_bruta = tk.StringVar()
gastos_operativos = tk.StringVar()
utilidad_operativa = tk.StringVar()
otros_gastos = tk.StringVar()
otros_ingresos = tk.StringVar()
utilidad_antes_impuestos = tk.StringVar()

# Crear y organizar la interfaz gráfica con etiquetas y campos
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

# Botón para cargar datos
tk.Button(root, text="Cargar Estado de Resultados", command=obtener_datos_estado_resultados).grid(row=9, column=0, columnspan=2, pady=10)

# Botón para regresar
btn_guardar = tk.Button(root, text="Regresar", command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r))
btn_guardar.pack(pady=10)

# Iniciar la aplicación de Tkinter
root.mainloop()
