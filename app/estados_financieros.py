import tkinter as tk
from tkinter import messagebox
from conexion import conectar_db
from navegacion import cambiar_pantalla

def calcular_y_guardar_situacion_financiera():
    try:
        # Conexión a la base de datos
        conexion = conectar_db()
        cursor = conexion.cursor()
        
        # Obtener total activo corriente
        cursor.execute("""
            SELECT SUM("Tran_MontoCre" - "Tran_MontoDeb") 
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
            WHERE c."Cuenta_CuentaTipoId" = 1 or c."Cuenta_CuentaTipoId" = 2;  -- Activo corriente sin y como existencias bb
        """)
        total_activo_corriente = cursor.fetchone()[0] or 0
        
        # Obtener total activo no corriente
        cursor.execute("""
            SELECT SUM("Tran_MontoCre" - "Tran_MontoDeb") 
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
            WHERE c."Cuenta_CuentaTipoId" = 3;  -- Activo no corriente
        """)
        total_activo_no_corriente = cursor.fetchone()[0] or 0
        
        # Obtener total pasivo corriente
        cursor.execute("""
            SELECT SUM("Tran_MontoDeb" - "Tran_MontoCre") 
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
            WHERE c."Cuenta_CuentaTipoId" = 4;  -- Pasivo corriente
        """)
        total_pasivo_corriente = cursor.fetchone()[0] or 0

        # Obtener total pasivo no corriente
        cursor.execute("""
            SELECT SUM("Tran_MontoDeb" - "Tran_MontoCre") 
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
            WHERE c."Cuenta_CuentaTipoId" = 5;  -- Pasivo no corriente
        """)
        total_pasivo_no_corriente = cursor.fetchone()[0] or 0
        
        # Obtener total patrimonio
        cursor.execute("""
            SELECT SUM("Tran_MontoCre" - "Tran_MontoDeb") 
            FROM transacciones t
            JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
            WHERE c."Cuenta_CuentaTipoId" = 6;  -- Patrimonio
        """)
        total_patrimonio = cursor.fetchone()[0] or 0

        # Calcular el activo total y el pasivo total
        activo_total = total_activo_corriente + total_activo_no_corriente
        pasivo_total = total_pasivo_corriente + total_pasivo_no_corriente
        
        # Insertar los datos en la tabla situacion_financiera
        cursor.execute("""
            INSERT INTO situacion_financiera (
                "SitFin_RegId", "SitFin_TotalActCorr", "SitFin_TotalActNoCorr", "SitFin_TotalAct",
                "SitFin_TotalPasCorr", "SitFin_TotalPasNoCorr", "SitFin_TotalPas", "SitFin_TotalPatrimonio"
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (1, total_activo_corriente, total_activo_no_corriente, activo_total, 
              total_pasivo_corriente, total_pasivo_no_corriente, pasivo_total, total_patrimonio))
        
        # Confirmar los cambios
        conexion.commit()

        print("Datos de situación financiera guardados correctamente.")

    except Exception as e:
        print("Error al calcular o guardar la situación financiera:", e)
    finally:
        cursor.close()
        conexion.close()

def mostrar_situacion_financiera(root, regid):
    try:
        # Conexión a la base de datos
        conexion = conectar_db()
        if conexion is None:
            return
        
        cursor = conexion.cursor()

        # Obtener los datos más recientes de la tabla situacion_financiera
        cursor.execute("""
            SELECT "SitFin_TotalActCorr", "SitFin_TotalActNoCorr", "SitFin_TotalAct",
                   "SitFin_TotalPasCorr", "SitFin_TotalPasNoCorr", "SitFin_TotalPas",
                   "SitFin_TotalPatrimonio"
            FROM situacion_financiera
            ORDER BY "SitFin_Id" DESC
            LIMIT 1;
        """, (regid,))
        datos = cursor.fetchone()

        if datos is None:
            messagebox.showwarning("Advertencia", "No se encontraron datos financieros para este registro.")
            return

        # Limpiar la ventana actual para mostrar la nueva pantalla
        for widget in root.winfo_children():
            widget.destroy()

        # Crear el título de la pantalla
        titulo = tk.Label(root, text="ESTADO DE SITUACIÓN FINANCIERA", font=("Helvetica", 16), fg="green")
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Mostrar los datos del activo
        tk.Label(root, text="ACTIVO", font=("Helvetica", 14, "bold"), fg="green").grid(row=1, column=0, sticky="w")
        tk.Label(root, text="TOTAL ACTIVO CORRIENTE:", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w")
        tk.Label(root, text=f"{datos[0]:,.2f}", font=("Helvetica", 12)).grid(row=2, column=1, sticky="e")

        tk.Label(root, text="TOTAL ACTIVO NO CORRIENTE:", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w")
        tk.Label(root, text=f"{datos[1]:,.2f}", font=("Helvetica", 12)).grid(row=3, column=1, sticky="e")

        tk.Label(root, text="ACTIVO TOTAL:", font=("Helvetica", 12, "bold")).grid(row=4, column=0, sticky="w")
        tk.Label(root, text=f"{datos[2]:,.2f}", font=("Helvetica", 12, "bold")).grid(row=4, column=1, sticky="e")

        # Mostrar los datos del pasivo
        tk.Label(root, text="PASIVO", font=("Helvetica", 14, "bold"), fg="orange").grid(row=5, column=0, sticky="w")
        tk.Label(root, text="TOTAL PASIVO CORRIENTE:", font=("Helvetica", 12)).grid(row=6, column=0, sticky="w")
        tk.Label(root, text=f"{datos[3]:,.2f}", font=("Helvetica", 12)).grid(row=6, column=1, sticky="e")

        tk.Label(root, text="TOTAL PASIVO NO CORRIENTE:", font=("Helvetica", 12)).grid(row=7, column=0, sticky="w")
        tk.Label(root, text=f"{datos[4]:,.2f}", font=("Helvetica", 12)).grid(row=7, column=1, sticky="e")

        tk.Label(root, text="PASIVO TOTAL:", font=("Helvetica", 12, "bold")).grid(row=8, column=0, sticky="w")
        tk.Label(root, text=f"{datos[5]:,.2f}", font=("Helvetica", 12, "bold")).grid(row=8, column=1, sticky="e")

        # Mostrar los datos del patrimonio
        tk.Label(root, text="PATRIMONIO", font=("Helvetica", 14, "bold"), fg="red").grid(row=9, column=0, sticky="w")
        tk.Label(root, text="TOTAL PATRIMONIO:", font=("Helvetica", 12)).grid(row=10, column=0, sticky="w")
        tk.Label(root, text=f"{datos[6]:,.2f}", font=("Helvetica", 12)).grid(row=10, column=1, sticky="e")

        # Mostrar total de pasivo + patrimonio
        tk.Label(root, text="TOTAL PASIVO + PATRIMONIO:", font=("Helvetica", 12, "bold")).grid(row=11, column=0, sticky="w")
        tk.Label(root, text=f"{datos[5] + datos[6]:,.2f}", font=("Helvetica", 12, "bold")).grid(row=11, column=1, sticky="e")

        # Botón para regresar
        btn_regresar = tk.Button(root, text="Regresar", command=lambda r=regid: cambiar_pantalla(root, 'ver_registro', r))
        btn_regresar.grid(row=12, column=0, columnspan=2, pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Error al mostrar la situación financiera: {e}")
    finally:
        cursor.close()
        conexion.close()