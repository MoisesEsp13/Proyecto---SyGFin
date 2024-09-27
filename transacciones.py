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
label = Label(frame, text="+")
label.grid(row=2, column=3)


# Debe
label = Label(frame, text="Debe")
label.grid(row=1, column=4)

entry_debe = Entry(frame)
entry_debe.grid(row=2, column=4)


# Haber
label = Label(frame, text="Haber")
label.grid(row=1, column=5)

entry_haber = Entry(frame)
entry_haber.grid(row=2, column=5)


root.mainloop()