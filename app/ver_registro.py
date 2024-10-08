import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from funciones_trans import *
from navegacion import cambiar_pantalla
from tkcalendar import DateEntry
from tkinter import messagebox

def mostrar_ver_registro(root, reg_id):
    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()
    
    conn = conectar_db()
    cur = conn.cursor()
    cur.execute("""SELECT "Reg_Nombre" FROM registros WHERE "Reg_Id" = %s""", (reg_id,))  
    nombre_entidad = cur.fetchall()
    cur.close()
    conn.close()

    # Título
    titulo = ctk.CTkLabel(root, text=f"Transacciones del Registro {nombre_entidad[0][0]}", 
                          font=("Helvetica", 30, "bold"), text_color="#2B6CB0")
    titulo.pack(pady=10)

    # Tabla de transacciones
    transacciones = obtener_transacciones(reg_id)
    
    estilo = ttk.Style()
    estilo.theme_use('clam')
    estilo.configure("Treeview", background="#2E2E2E", foreground="white", 
                     fieldbackground="#2E2E2E", rowheight=25)
    estilo.configure("Treeview.Heading", background="#1C1C1C", foreground="white")

    estilo = ttk.Style()
    estilo.configure("White.Treeview", background="white", fieldbackground="white", foreground="dark blue")

    # Crear tabla
    tabla = ttk.Treeview(root, columns=("Fecha", "Cuenta", "Debe", "Haber"), show="headings", style="White.Treeview")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Cuenta", text="Cuenta")
    tabla.heading("Debe", text="Debe")
    tabla.heading("Haber", text="Haber")

    # Ajustar ancho
    tabla.column("Fecha", width=90, anchor="center")
    tabla.column("Cuenta", width=400)
    tabla.column("Debe", width=120, anchor="center") 
    tabla.column("Haber", width=120, anchor="center")

    # Insertar los datos en la tabla
    for trans in transacciones:
        tabla.insert("", "end", values=trans)

    tabla.pack(pady=10)
    
    # Adiccionar transacciones
    agregar_transaccion(root, reg_id, tabla)

    # Botones
    btn_mayores = ctk.CTkButton(root, text="Mostrar Mayores", 
                                command=lambda: cambiar_pantalla(root, 'mayores', reg_id),
                                fg_color="#4A5568", hover_color="#2D3748", text_color="white")
    btn_mayores.pack(side=ctk.LEFT, padx=10)

    btn_balanza = ctk.CTkButton(root, text="Balanza de Comprobación", 
                            command=lambda: cambiar_pantalla(root, 'balanza_comprobacion', reg_id),
                                fg_color="#4A5568", hover_color="#2D3748", text_color="white")
    btn_balanza.pack(side=tk.LEFT, padx=10)

    btn_situacion_financiera = ctk.CTkButton(root, text="Mostrar Estados Financieros",
                                             command=lambda: cambiar_pantalla(root, 'situacion_financiera', reg_id),
                                             fg_color="#4A5568", hover_color="#2D3748", text_color="white")
    btn_situacion_financiera.pack(side=ctk.LEFT, padx=10)

    # Botón para abrir el estado de resultados
    btn_estado_resultados = ctk.CTkButton(root, text="Ver Estado de Resultados",
                                          command=lambda: cambiar_pantalla(root, 'estado_resultados', reg_id),
                                          fg_color="#4A5568", hover_color="#2D3748", text_color="white")
    btn_estado_resultados.pack(side=ctk.LEFT, padx=10)

    # Botón para regresar
    btn_regresar = ctk.CTkButton(root, text="Regresar", 
                                 command=lambda: cambiar_pantalla(root, 'bienvenida'),
                                 fg_color="#4A5568", hover_color="#2D3748", text_color="white")
    btn_regresar.pack(side=ctk.LEFT, padx=10)


def guardar_datos(reg_id, cmb_cuenta_id, cmb_is_aum, entry_monto, entry_fecha, tabla):
    cuenta_id = cmb_cuenta_id.get()
    monto = entry_monto.get()
    is_aum = cmb_is_aum.get()
    fecha = entry_fecha.get()

    if fecha and cuenta_id and is_aum and monto:
        try:
            is_aum_bool = True if is_aum == "+" else False
            guardar_transaccion(reg_id, cuenta_id, monto, is_aum_bool, fecha)
            print("Datos enviados correctamente")

            # Vaciar la tabla actual
            for item in tabla.get_children():
                tabla.delete(item)

            # Obtener transacciones actualizadas y mostrarlas
            transacciones = obtener_transacciones(reg_id)
            for trans in transacciones:
                tabla.insert("", "end", values=trans)

        except Exception as e:
            print("Error al guardar los datos:", e)
    else:
        messagebox.showwarning("Advertencia", "Faltan campos por completar.")
        print("Faltan campos por completar")



def agregar_transaccion(root, reg_id, tabla):

    frame = tk.Frame(
        root,
        padx=7, pady=3,
        bg="#f0f8ff",
        highlightbackground="#1e3d73",
        highlightthickness=3
    )
    frame.pack(pady=10)

    label_style = {"font": ("Arial", 10, "bold"), "bg": "#f0f8ff", "fg": "#1e3d73"}

    # Fecha
    label_fecha = tk.Label(frame, text="Fecha", **label_style)
    label_fecha.grid(row=1, column=0, padx=5, pady=5)

    entry_fecha = DateEntry(
        frame,
        width=12,
        background="#1e3d73",
        foreground="white",
        date_pattern="yyyy-mm-dd",
        borderwidth=2,
    )
    entry_fecha.grid(row=2, column=0, padx=5, pady=5)

    # Cuenta
    label_cuenta = tk.Label(frame, text="Cuenta", **label_style)
    label_cuenta.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

    # Comboboxes
    combo_style = ttk.Style()
    combo_style.configure("TCombobox", fieldbackground="#e1ecf7", background="white", foreground="#1e3d73")

    cmb_cuenta_tipo = ttk.Combobox(frame, width=30, state="readonly", style="TCombobox")
    cmb_cuenta_tipo.grid(row=2, column=1, padx=5, pady=5)

    cmb_cuenta_id = ttk.Combobox(frame, width=3, state="readonly", style="TCombobox")
    cmb_cuenta_id.grid(row=2, column=2, padx=5, pady=5)

    cmb_cuenta_nom = ttk.Combobox(frame, width=45, state="readonly", style="TCombobox")
    cmb_cuenta_nom.grid(row=2, column=3, padx=5, pady=5)

    # Diccionario para tipos de cuenta
    tipos_cuenta = {tipo[1]: tipo[0] for tipo in obtener_tipos_cuenta()}
    cmb_cuenta_tipo['values'] = list(tipos_cuenta.keys())

    cuentas = obtener_cuentas(None)
    cmb_cuenta_id['values'] = [cuenta[0] for cuenta in cuentas]
    cmb_cuenta_nom['values'] = [cuenta[1] for cuenta in cuentas]

    cmb_cuenta_id.bind("<<ComboboxSelected>>", lambda event: sincronizar_nom(event, cmb_cuenta_nom, cmb_cuenta_id, cuentas))
    cmb_cuenta_nom.bind("<<ComboboxSelected>>", lambda event: sincronizar_id(event, cmb_cuenta_nom, cmb_cuenta_id, cuentas))

    cmb_cuenta_tipo.bind("<<ComboboxSelected>>", lambda event: tipo_cuenta_seleccion(event, cmb_cuenta_tipo, cmb_cuenta_id, cmb_cuenta_nom, tipos_cuenta))

    # IsAumento
    cmb_is_aum = ttk.Combobox(frame, width=3, state="readonly", values=["+", "-"], style="TCombobox")
    cmb_is_aum.grid(row=2, column=4, padx=5, pady=5)

    # Monto
    label_monto = tk.Label(frame, text="Monto", **label_style)
    label_monto.grid(row=1, column=5, padx=5, pady=5)

    entry_monto = tk.Entry(frame, bg="#e1ecf7", fg="#1e3d73", borderwidth=2, relief="groove")
    entry_monto.grid(row=2, column=5, padx=5, pady=5)

    # Botón para guardar
    btn_guardar = tk.Button(
        frame,
        text="Guardar",
        command=lambda: guardar_datos(reg_id, cmb_cuenta_id, cmb_is_aum, entry_monto, entry_fecha, tabla),
        bg="#1e3d73", 
        fg="white",
        font=("Arial", 10, "bold"),
        relief="ridge",
        padx=10,
        pady=5
    )
    btn_guardar.grid(row=3, column=5, pady=15, padx=10)
