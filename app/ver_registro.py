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

    # Título
    titulo = tk.Label(root, text=f"Transacciones del Registro {reg_id}", font=("Helvetica", 16))
    titulo.pack(pady=10)

    # Tabla de transacciones
    transacciones = obtener_transacciones(reg_id)
    tabla = ttk.Treeview(root, columns=("Fecha", "Cuenta", "Debe", "Haber"), show="headings")
    tabla.heading("Fecha", text="Fecha")
    tabla.heading("Cuenta", text="Cuenta")
    tabla.heading("Debe", text="Debe")
    tabla.heading("Haber", text="Haber")

    for trans in transacciones:
        tabla.insert("", "end", values=trans)

    tabla.pack(pady=10)
    
    # Adiccionar transacciones
    agregar_transaccion(root, reg_id, tabla)

    # Botones
    btn_mayores = tk.Button(root, text="Mostrar Mayores", command=lambda: cambiar_pantalla(root, 'mayores', reg_id))
    btn_mayores.pack(side=tk.LEFT, padx=10)

    btn_balanza = tk.Button(root, text="Balanza de Comprobación", 
                            command=lambda: cambiar_pantalla(root, 'balanza_comprobacion', reg_id))
    btn_balanza.pack(side=tk.LEFT, padx=10)

    btn_situacion_financiera = tk.Button(root, text="Mostrar Estados Financieros",
                                         command=lambda: cambiar_pantalla(root, 'situacion_financiera', reg_id))
    btn_situacion_financiera.pack(side=tk.LEFT, padx=10)

    # Botón para abrir el estado de resultados
    btn_estado_resultados = tk.Button(root, text="Ver Estado de Resultados",
                                      command=lambda: cambiar_pantalla(root, 'estado_resultados', reg_id))
    btn_estado_resultados.pack(side=tk.LEFT, padx=10)

    # Botón para regresar
    btn_regresar = tk.Button(root, text="Regresar", command=lambda: cambiar_pantalla(root, 'bienvenida'))
    btn_regresar.pack(side=tk.LEFT, padx=10)


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
    
    frame = tk.Frame(root)
    frame.pack(pady=10)

    # Fecha
    label_fecha = tk.Label(frame, text="Fecha")
    label_fecha.grid(row=1, column=0)

    entry_fecha = DateEntry(frame, width=12, background="dark gray",
                            foreground="white", date_pattern="yyyy-mm-dd",
                            borderwidth=2)
    entry_fecha.grid(row=2, column=0)

    # Cuenta
    label_cuenta = tk.Label(frame, text="Cuenta")
    label_cuenta.grid(row=1, column=1, columnspan=3)

    cmb_cuenta_tipo = ttk.Combobox(frame, width="30", state="readonly")
    cmb_cuenta_tipo.grid(row=2, column=1)
    
    cmb_cuenta_id = ttk.Combobox(frame, width="3", state="readonly")
    cmb_cuenta_id.grid(row=2, column=2)

    cmb_cuenta_nom = ttk.Combobox(frame, width="45", state="readonly")
    cmb_cuenta_nom.grid(row=2, column=3)

    # Diccionario para tipos de cuenta
    tipos_cuenta = {tipo[1]: tipo[0] for tipo in obtener_tipos_cuenta()}
    cmb_cuenta_tipo['values'] = list(tipos_cuenta.keys())

    cuentas = obtener_cuentas(None)
    cmb_cuenta_id['values'] = [cuenta[0] for cuenta in cuentas]
    cmb_cuenta_nom['values'] = [cuenta[1] for cuenta in cuentas]

    cmb_cuenta_id.bind("<<ComboboxSelected>>", lambda event: sincronizar_nom(event, cmb_cuenta_nom, cmb_cuenta_id, cuentas))
    cmb_cuenta_nom.bind("<<ComboboxSelected>>", lambda event: sincronizar_id(event, cmb_cuenta_nom, cmb_cuenta_id, cuentas))

    # Manejar de la selección
    cmb_cuenta_tipo.bind("<<ComboboxSelected>>", lambda event: tipo_cuenta_seleccion(event, cmb_cuenta_tipo, cmb_cuenta_id, cmb_cuenta_nom, tipos_cuenta))

    # IsAumento
    cmb_is_aum = ttk.Combobox(frame, width="3", state="readonly", values=["+", "-"])
    cmb_is_aum.grid(row=2, column=4)

    # Monto
    label_monto = tk.Label(frame, text="Monto")
    label_monto.grid(row=1, column=5)

    entry_monto = tk.Entry(frame)
    entry_monto.grid(row=2, column=5)

    # Botón para guardar
    btn_guardar = tk.Button(frame, text="Guardar", command=lambda: guardar_datos(reg_id, cmb_cuenta_id, cmb_is_aum, entry_monto, entry_fecha, tabla))
    btn_guardar.grid(row=3, column=5, pady=10)
