import tkinter as tk
from tkinter import ttk
from conexion import conectar_db
from navegacion import cambiar_pantalla

def obtener_registros():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT "Reg_Id", "Reg_Nombre" FROM registros ORDER BY "Reg_Fecha" DESC')
    registros = cursor.fetchall()
    conn.close()
    return registros

def mostrar_bienvenida(root):
    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()

    # Título
    titulo = tk.Label(root, text="Bienvenido al Sistema Contable", font=("Helvetica", 16))
    titulo.pack(pady=10)

    # Listar registros como botones
    registros = obtener_registros()
    for reg_id, nombre in registros:
        boton_registro = ttk.Button(root, text=nombre,
                                    command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r))
        boton_registro.pack(pady=5)

    # Botón para crear nuevo registro
    btn_crear = tk.Button(root, text="Crear Nuevo Registro",
                              command=lambda: cambiar_pantalla(root, 'crear_registro'))
    btn_crear.pack(pady=10)