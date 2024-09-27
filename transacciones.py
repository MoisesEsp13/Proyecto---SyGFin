from tkinter import *
from conexion import *

root = Tk()
root.title("Agregar Transacciones")

# Canva
canvas = Canvas(root, height=380, width=600)
canvas.pack()

frame = Frame()
frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)


# Fecha
label = Label(frame, text="Fecha")
label.grid(row=1, column=0)

entry_fecha = Entry(frame)
entry_fecha.grid(row=2, column=0)

# Cuenta
label = Label(frame, text="Cuenta")
label.grid(row=1, column=1)

entry_cuenta = Entry(frame)
entry_cuenta.grid(row=2, column=1)

# IsAumento
label = Label(frame, text="+")
label.grid(row=2, column=2)

# Debe
label = Label(frame, text="Debe")
label.grid(row=1, column=3)

entry_debe = Entry(frame)
entry_debe.grid(row=2, column=3)

# Haber
label = Label(frame, text="Haber")
label.grid(row=1, column=4)

entry_haber = Entry(frame)
entry_haber.grid(row=2, column=4)

root.mainloop()