from tkinter import *
from tran_guardar import *
from tran_mostrar import *
from tkinter.ttk import Combobox
from tkcalendar import DateEntry

root = Tk()
root.title("Agregar Transacciones")

# Funciones

def sincronizar_id(event):
    nombre_seleccionado = cmb_cuenta_nom.get()
    for cuenta in cuentas:
        if cuenta[1] == nombre_seleccionado:
            cmb_cuenta_id.set(cuenta[0])
            break

def sincronizar_nom(event):
    id_seleccionado = cmb_cuenta_id.get()
    for cuenta in cuentas:
        if str(cuenta[0]) == id_seleccionado:
            cmb_cuenta_nom.set(cuenta[1])
            break

def guardar_datos():
    reg_id = 1
    cuenta_id = cmb_cuenta_id.get()
    monto = entry_monto.get()
    is_aum = True if cmb_is_aum.get() == "+" else False
    fecha = entry_fecha.get()

    if fecha and cuenta_id and is_aum and monto:
        try:
            guardar_transaccion(reg_id, cuenta_id, monto, is_aum, fecha)
            print("Datos guardados correctamente")

        except Exception as e:
            print("Error al guardar los datos:", e)
    else:
        print("Faltan campos por completar")

# Canva
canvas = Canvas(root, height=380, width=900)
canvas.pack()

frame = Frame()
frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)


# Fecha
label = Label(frame, text="Fecha")
label.grid(row=1, column=0)

entry_fecha = DateEntry(frame, width=12, background="dark gray",
                        foreground="white", dateformat="%Y-%m-%d",
                        botderwidth=2, botdercolor="black")
entry_fecha.grid(row=2, column=0)


# Cuenta
label = Label(frame, text="Cuenta")
label.grid(row=1, column=1)

cmb_cuenta_id = Combobox(frame, width="3", state="readonly")
cmb_cuenta_id.grid(row=2, column=1)

cmb_cuenta_nom = Combobox(frame, width="45", state="readonly")
cmb_cuenta_nom.grid(row=2, column=2)


cuentas = obtener_cuentas()

cmb_cuenta_id['values'] = [cuenta[0] for cuenta in cuentas]
cmb_cuenta_id.bind("<<ComboboxSelected>>", sincronizar_nom)

cmb_cuenta_nom['values'] = [cuenta[1] for cuenta in cuentas]
cmb_cuenta_nom.bind("<<ComboboxSelected>>", sincronizar_id)


# IsAumento
cmb_is_aum = Combobox(frame, width="2", state="readonly", 
                      values=["+", "-"])
cmb_is_aum.grid(row=2, column=3)


# Monto
label = Label(frame, text="Monto")
label.grid(row=1, column=4)

entry_monto = Entry(frame)
entry_monto.grid(row=2, column=4)


# Botón
btn_guardar = Button(frame, text="Guardar", command=guardar_datos)
btn_guardar.grid(row=3, column=4, pady=10)


root.mainloop()