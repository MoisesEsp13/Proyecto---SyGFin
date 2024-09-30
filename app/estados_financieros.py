import tkinter as tk
from navegacion import cambiar_pantalla

def calcular_situacion_financiera(activo_corriente, inventarios, activo_fijo, deprec_acumulada, pasivo_corriente,
                                  capital_social, utilidades_acumuladas):
    # Activo
    total_activo_corriente = activo_corriente + inventarios
    total_activo_no_corriente = activo_fijo - deprec_acumulada
    activo_total = total_activo_corriente + total_activo_no_corriente

    # Pasivo
    total_pasivo = pasivo_corriente

    # Patrimonio
    total_patrimonio = capital_social + utilidades_acumuladas

    # Verificación de la ecuación fundamental
    if activo_total == total_pasivo + total_patrimonio:
        return {
            "total_activo_corriente": total_activo_corriente,
            "total_activo_no_corriente": total_activo_no_corriente,
            "activo_total": activo_total,
            "total_pasivo": total_pasivo,
            "total_patrimonio": total_patrimonio
        }
    else:
        raise ValueError("Los activos no coinciden con pasivos + patrimonio.")


def mostrar_situacion_financiera(root,reg_id):
    # Valores de ejemplo para la demostración
    activo_corriente = 10900
    inventarios = 2500
    activo_fijo = 3000
    deprec_acumulada = 135
    pasivo_corriente = 3200
    capital_social = 10000
    utilidades_acumuladas = 3065

    # Calcular situación financiera
    valores = calcular_situacion_financiera(activo_corriente, inventarios, activo_fijo, deprec_acumulada,
                                            pasivo_corriente, capital_social, utilidades_acumuladas)

    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()

    # Título
    titulo = tk.Label(root, text="ESTADO DE SITUACIÓN FINANCIERA", font=("Helvetica", 16), fg="green")
    titulo.grid(row=0, column=0, columnspan=2, pady=10)

    # Activo
    tk.Label(root, text="ACTIVO", font=("Helvetica", 14, "bold"), fg="green").grid(row=1, column=0, sticky="w")
    tk.Label(root, text="TOTAL ACTIVO CORRIENTE:", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w")
    tk.Label(root, text=f"{valores['total_activo_corriente']:.2f}", font=("Helvetica", 12)).grid(row=2, column=1,
                                                                                                 sticky="e")

    tk.Label(root, text="TOTAL ACTIVO NO CORRIENTE:", font=("Helvetica", 12)).grid(row=3, column=0, sticky="w")
    tk.Label(root, text=f"{valores['total_activo_no_corriente']:.2f}", font=("Helvetica", 12)).grid(row=3, column=1,
                                                                                                    sticky="e")

    tk.Label(root, text="ACTIVO TOTAL:", font=("Helvetica", 12, "bold")).grid(row=4, column=0, sticky="w")
    tk.Label(root, text=f"{valores['activo_total']:.2f}", font=("Helvetica", 12, "bold")).grid(row=4, column=1,
                                                                                               sticky="e")

    # Pasivo
    tk.Label(root, text="PASIVO", font=("Helvetica", 14, "bold"), fg="orange").grid(row=5, column=0, sticky="w")
    tk.Label(root, text="TOTAL PASIVO:", font=("Helvetica", 12)).grid(row=6, column=0, sticky="w")
    tk.Label(root, text=f"{valores['total_pasivo']:.2f}", font=("Helvetica", 12)).grid(row=6, column=1, sticky="e")

    # Patrimonio
    tk.Label(root, text="PATRIMONIO", font=("Helvetica", 14, "bold"), fg="red").grid(row=7, column=0, sticky="w")
    tk.Label(root, text="TOTAL PATRIMONIO:", font=("Helvetica", 12)).grid(row=8, column=0, sticky="w")
    tk.Label(root, text=f"{valores['total_patrimonio']:.2f}", font=("Helvetica", 12)).grid(row=8, column=1, sticky="e")

    # Total Pasivo + Patrimonio
    tk.Label(root, text="TOTAL PASIVO + PATRIMONIO:", font=("Helvetica", 12, "bold")).grid(row=9, column=0, sticky="w")
    tk.Label(root, text=f"{valores['total_pasivo'] + valores['total_patrimonio']:.2f}",
             font=("Helvetica", 12, "bold")).grid(row=9, column=1, sticky="e")

    # Botón para regresar
    btn_guardar = tk.Button(root, text="Regresar", command=lambda r=reg_id: cambiar_pantalla(root, 'ver_registro', r))
    btn_guardar.grid(row=10, column=0, columnspan=2, pady=10)
