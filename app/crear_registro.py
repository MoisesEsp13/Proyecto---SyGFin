import tkinter as tk
from tkinter import ttk
from conexion import conectar_db
from navegacion import cambiar_pantalla

def guardar_registro(moneda, nombre, cmb_moneda, entry_nombre):
    conn = conectar_db()
    cursor = conn.cursor()
    query = '''INSERT INTO registros("Reg_MonedaId", "Reg_Nombre", "Reg_Fecha") VALUES (%s, %s, CURRENT_DATE)'''
    cursor.execute(query, (moneda, nombre))
    conn.commit()
    conn.close()

    cmb_moneda.set('')
    entry_nombre.delete(0, tk.END)

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
    label_nombre = tk.Label(root, text="Nombre")
    label_nombre.pack()
    entry_nombre = tk.Entry(root, width=50)
    entry_nombre.pack()

    # Botón para guardar
    btn_guardar = tk.Button(root, text="Guardar", command=lambda: guardar_registro(monedas[cmb_moneda.get()], entry_nombre.get(),cmb_moneda,entry_nombre))
    btn_guardar.pack(pady=10)

    # Botón para regresar
    btn_guardar = tk.Button(root, text="Regresar", command=lambda: cambiar_pantalla(root, 'bienvenida'))
    btn_guardar.pack(pady=10)
