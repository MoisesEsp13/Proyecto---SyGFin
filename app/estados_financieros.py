import tkinter as tk
from tkinter import ttk, messagebox
from conexion import conectar_db
from navegacion import cambiar_pantalla

def obtener_anios(cursor):
    """Función para obtener los años de las transacciones"""
    cursor.execute("""
        SELECT DISTINCT EXTRACT(YEAR FROM t."Tran_Fecha")::INTEGER AS anio
        FROM transacciones t
        ORDER BY anio;
    """)
    return [row[0] for row in cursor.fetchall()]

def obtener_datos_por_anio(cursor, anio):
    """Función para obtener los valores de activos, pasivos y patrimonio de un año específico"""
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN c."Cuenta_CuentaTipoId" IN (1, 2) THEN "Tran_MontoCre" - "Tran_MontoDeb" ELSE 0 END) AS total_activo_corriente,
            SUM(CASE WHEN c."Cuenta_CuentaTipoId" = 3 THEN "Tran_MontoCre" - "Tran_MontoDeb" ELSE 0 END) AS total_activo_no_corriente,
            SUM(CASE WHEN c."Cuenta_CuentaTipoId" = 4 THEN "Tran_MontoDeb" - "Tran_MontoCre" ELSE 0 END) AS total_pasivo_corriente,
            SUM(CASE WHEN c."Cuenta_CuentaTipoId" = 5 THEN "Tran_MontoDeb" - "Tran_MontoCre" ELSE 0 END) AS total_pasivo_no_corriente,
            SUM(CASE WHEN c."Cuenta_CuentaTipoId" = 6 THEN "Tran_MontoCre" - "Tran_MontoDeb" ELSE 0 END) AS total_patrimonio
        FROM transacciones t
        JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
        WHERE EXTRACT(YEAR FROM t."Tran_Fecha") = %s;
    """, (anio,))
    return cursor.fetchone()

def mostrar_situacion_financiera(root, regid):
    try:
        # Conexión a la base de datos
        conexion = conectar_db()
        if conexion is None:
            return
        
        cursor = conexion.cursor()

        # Obtener los años disponibles
        anios = obtener_anios(cursor)
        if not anios:
            messagebox.showwarning("Advertencia", "No se encontraron transacciones.")
            return

        # Crear la lista de selección de año
        def actualizar_tabla(event):
            anio_seleccionado = combo_anios.get()
            if anio_seleccionado:
                cargar_datos(int(anio_seleccionado))

        def cargar_datos(anio):
            # Obtener los datos financieros del año seleccionado
            datos = obtener_datos_por_anio(cursor, anio)
            if datos is None:
                messagebox.showwarning("Advertencia", f"No se encontraron datos financieros para el año {anio}.")
                return

            # Limpiar la tabla antes de cargar nuevos datos
            for row in tabla.get_children():
                tabla.delete(row)

            # Insertar datos en la tabla
            tabla.insert("", "end", values=(
                f"{anio}",
                f"{datos[0]:,.2f}",
                f"{datos[1]:,.2f}",
                f"{datos[0] + datos[1]:,.2f}",
                f"{datos[2]:,.2f}",
                f"{datos[3]:,.2f}",
                f"{datos[2] + datos[3]:,.2f}",
                f"{datos[4]:,.2f}",
                f"{datos[2] + datos[3] + datos[4]:,.2f}"
            ))

        # Limpiar la ventana actual para mostrar la nueva pantalla
        for widget in root.winfo_children():
            widget.destroy()

        # Crear el título de la pantalla
        titulo = tk.Label(root, text="ESTADO DE SITUACIÓN FINANCIERA", font=("Helvetica", 16), fg="green")
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Lista desplegable para seleccionar el año
        tk.Label(root, text="Seleccione el año:", font=("Helvetica", 12)).grid(row=1, column=0, sticky="w")
        combo_anios = ttk.Combobox(root, values=anios)
        combo_anios.grid(row=1, column=1, sticky="e")
        combo_anios.bind("<<ComboboxSelected>>", actualizar_tabla)

        # Crear la tabla para mostrar los datos financieros
        columnas = (
            "Año", "Activo Corriente", "Activo No Corriente", "Activo Total",
            "Pasivo Corriente", "Pasivo No Corriente", "Pasivo Total",
            "Patrimonio", "Pasivo + Patrimonio"
        )
        tabla = ttk.Treeview(root, columns=columnas, show="headings", height=5)
        tabla.grid(row=2, column=0, columnspan=2, pady=10)

        # Configurar encabezados
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center")

        # Cargar datos para el primer año por defecto
        combo_anios.current(0)
        cargar_datos(anios[0])

        # Botón para regresar
        btn_regresar = tk.Button(root, text="Regresar", command=lambda r=regid: cambiar_pantalla(root, 'ver_registro', r))
        btn_regresar.grid(row=3, column=0, columnspan=2, pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Error al mostrar la situación financiera: {e}")
    finally:
        cursor.close()
        conexion.close()
