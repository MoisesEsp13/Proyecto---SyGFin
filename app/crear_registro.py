import tkinter as tk
from tkinter import ttk
from conexion import conectar_db
from navegacion import cambiar_pantalla

def guardar_registro(moneda, saldo_inicial):
    conn = conectar_db()
    cursor = conn.cursor()
    query = '''INSERT INTO registros("Reg_MonedaId", "Reg_SaldoIncial", "Reg_Fecha") VALUES (%s, %s, CURRENT_DATE)'''
    cursor.execute(query, (moneda, saldo_inicial))
    conn.commit()
    conn.close()

def mostrar_crear_registro(root):
    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()

    # Título
    titulo = tk.Label(root, text="Crear Nuevo Registro", font=("Helvetica", 16))
    titulo.pack(pady=10)

    # Moneda
    monedas = {"Soles S/.": 1, "Dólares $": 2}
    label_moneda = tk.Label(root, text="Moneda")
    label_moneda.pack()
    cmb_moneda = ttk.Combobox(root, values=list(monedas.keys()), state="readonly")
    cmb_moneda.pack()

    # Saldo inicial
    label_saldo = tk.Label(root, text="Saldo Inicial")
    label_saldo.pack()
    entry_saldo = tk.Entry(root)
    entry_saldo.pack()

    # Botón para guardar
    btn_guardar = tk.Button(root, text="Guardar", command=lambda: guardar_registro(monedas[cmb_moneda.get()], entry_saldo.get()))
    btn_guardar.pack(pady=10)

    # Botón para regresar
    btn_guardar = tk.Button(root, text="Regresar", command=lambda: cambiar_pantalla(root, 'bienvenida'))
    btn_guardar.pack(pady=10)
