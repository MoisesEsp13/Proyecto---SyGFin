import tkinter as tk
from tkinter import ttk
import psycopg2

# Conectar a la base de datos
def conectar_db():
    try:
        conn = psycopg2.connect(dbname="SistemaContable", user="postgres",
                                password="123456", host="localhost", port="5432")
        return conn
    except:
        print("Error al conectar a la base de datos")

# Función para obtener el estado de resultados
def obtener_estado_resultados():
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT "EstRes_Venta", "EstRes_CostoVenta", "EstRes_UtilidadBruta", 
               "EstRes_GastosVenta", "EstRes_GastosAdmi", "EstRes_UtilidadOper", 
               "EstRes_OtrosIngresosGastos", "EstRes_GastosFinancieros", "EstRes_UtilidadAnteImpuestos"
        FROM estado_resultados
        WHERE "EstRes_RegId" = 1  -- ID de ejemplo
    """)
    resultado = cur.fetchone()
    cur.close()
    conn.close()
    return resultado

# Función para mostrar el estado de resultados en la GUI
def mostrar_estado_resultados():
    resultado = obtener_estado_resultados()
    
    if resultado:
        ventas_netas_var.set(f"{resultado[0]:,.2f}")
        costo_venta_var.set(f"{resultado[1]:,.2f}")
        utilidad_bruta_var.set(f"{resultado[2]:,.2f}")
        gastos_operativos_var.set(f"{resultado[3] + resultado[4]:,.2f}")  # Gastos de venta + administrativos
        utilidad_operativa_var.set(f"{resultado[5]:,.2f}")
        otros_gastos_var.set(f"{resultado[6]:,.2f}")
        utilidad_antes_impuestos_var.set(f"{resultado[8]:,.2f}")
    else:
        print("No se encontraron resultados.")

# Crear la interfaz de usuario con Tkinter
root = tk.Tk()
root.title("Estado de Resultados")

# Variables para los valores
ventas_netas_var = tk.StringVar()
costo_venta_var = tk.StringVar()
utilidad_bruta_var = tk.StringVar()
gastos_operativos_var = tk.StringVar()
utilidad_operativa_var = tk.StringVar()
otros_gastos_var = tk.StringVar()
utilidad_antes_impuestos_var = tk.StringVar()

# Crear etiquetas y valores
ttk.Label(root, text="VENTAS NETAS").grid(row=0, column=0, sticky="w")
ttk.Label(root, textvariable=ventas_netas_var).grid(row=0, column=1)

ttk.Label(root, text="COSTO DE LA VENTA").grid(row=1, column=0, sticky="w")
ttk.Label(root, textvariable=costo_venta_var).grid(row=1, column=1)

ttk.Label(root, text="UTILIDAD BRUTA").grid(row=2, column=0, sticky="w")
ttk.Label(root, textvariable=utilidad_bruta_var).grid(row=2, column=1)

ttk.Label(root, text="GASTOS OPERATIVOS").grid(row=3, column=0, sticky="w")
ttk.Label(root, textvariable=gastos_operativos_var).grid(row=3, column=1)

ttk.Label(root, text="UTILIDAD OPERATIVA").grid(row=4, column=0, sticky="w")
ttk.Label(root, textvariable=utilidad_operativa_var).grid(row=4, column=1)

ttk.Label(root, text="OTROS GASTOS (-)").grid(row=5, column=0, sticky="w")
ttk.Label(root, textvariable=otros_gastos_var).grid(row=5, column=1)

ttk.Label(root, text="UTILIDAD ANTES DE IMPUESTOS").grid(row=6, column=0, sticky="w")
ttk.Label(root, textvariable=utilidad_antes_impuestos_var).grid(row=6, column=1)

# Botón para cargar los datos
ttk.Button(root, text="Cargar Estado de Resultados", command=mostrar_estado_resultados).grid(row=7, column=0, columnspan=2)

root.mainloop()
