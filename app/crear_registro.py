import customtkinter as ctk
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
    entry_nombre.delete(0, ctk.END)

def mostrar_crear_registro(root):
    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()

    # Título
    titulo = ctk.CTkLabel(root, text="Crear Nuevo Registro", 
                          font=("Helvetica", 24, "bold"), text_color="#2B6CB0")
    titulo.pack(pady=20)

    # Moneda
    monedas = {"Soles S/.": 1, "Dólares $": 2}
    label_moneda = ctk.CTkLabel(root, text="Moneda", font=("Helvetica", 14), text_color="#2D3748")
    label_moneda.pack(pady=5)
    
    cmb_moneda = ctk.CTkComboBox(root, values=list(monedas.keys()), state="readonly")
    cmb_moneda.pack(pady=10)

    # Nombre
    label_nombre = ctk.CTkLabel(root, text="Nombre", font=("Helvetica", 14), text_color="#2D3748")
    label_nombre.pack(pady=5)
    
    entry_nombre = ctk.CTkEntry(root, width=300)
    entry_nombre.pack(pady=10)

    # Botón para guardar
    btn_guardar = ctk.CTkButton(root, text="Guardar",
                                command=lambda: guardar_registro(monedas[cmb_moneda.get()], entry_nombre.get(), cmb_moneda, entry_nombre),
                                font=("Helvetica", 16),
                                fg_color="#4A5568", hover_color="#2C5282")
    btn_guardar.pack(pady=15)

    # Botón para regresar
    btn_regresar = ctk.CTkButton(root, text="Regresar", 
                                 command=lambda: cambiar_pantalla(root, 'bienvenida'),
                                 font=("Helvetica", 16),
                                 fg_color="#A0AEC0", hover_color="#718096")
    btn_regresar.pack(pady=10)
