import customtkinter as ctk
from navegacion import cambiar_pantalla

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Sistema Contable")
    root.geometry("900x600")

    # Mostrar la pantalla de bienvenida al iniciar
    cambiar_pantalla(root, 'bienvenida')

    root.mainloop()

if __name__ == "__main__":
    main()

    
