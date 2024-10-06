import tkinter as tk
from navegacion import cambiar_pantalla

def main():
    root = tk.Tk()
    root.title("Sistema Contable")
    root.geometry("900x600")

    # Mostrar la pantalla de bienvenida al iniciar
    cambiar_pantalla(root, 'bienvenida')

    root.mainloop()

if __name__ == "__main__":
    main()
    