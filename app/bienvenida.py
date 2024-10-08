import customtkinter as ctk
from conexion import conectar_db
from navegacion import cambiar_pantalla
from PIL import Image

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
    titulo = ctk.CTkLabel(root, text="Bienvenido al Sistema Contable", 
                          font=("Helvetica", 30, "bold"), text_color="#2B6CB0")
    titulo.pack(pady=(20, 10))

    # Cargar imagen
    imagen_path = "app/imagenes/logo6.png"
    imagen_logo = ctk.CTkImage(Image.open(imagen_path), size=(200, 200))
    logo_label = ctk.CTkLabel(root, image=imagen_logo, text="")
    logo_label.pack(pady=10)

    # Listar registros como botones
    registros = obtener_registros()
    for reg_id, nombre in registros:
        boton_registro = ctk.CTkButton(
            root,
            text=nombre,
            command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r),
            font=("Helvetica", 14),
            fg_color="#4A5568",
            hover_color="#2D3748"
        )
        boton_registro.pack(pady=5)

    # Botón para crear nuevo registro
    btn_crear = ctk.CTkButton(
        root,
        text="Crear Nuevo Registro",
        command=lambda: cambiar_pantalla(root, 'crear_registro'),
        font=("Helvetica", 16, "bold"),
        text_color="white",
        corner_radius=8,
        height=25,
        width=150
    )
    btn_crear.pack(pady=(15, 10))
