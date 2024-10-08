def cambiar_pantalla(root, pantalla, *args):
    """
    Cambia entre las pantallas de la aplicación.
    :param root: La ventana principal.
    :param pantalla: La pantalla que se quiere mostrar (bienvenida, crear_registro, ver_registro, mayores, situacion_financiera).
    :param args: Argumentos adicionales para la pantalla seleccionada.
    """
    # Limpiar la ventana
    for widget in root.winfo_children():
        widget.destroy()

    # Eliminar formateo de root
    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=0)
    root.grid_columnconfigure(0, weight=0)
    root.grid_columnconfigure(1, weight=0)

    # Cambiar a la pantalla seleccionada
    if pantalla == 'bienvenida':
        from bienvenida import mostrar_bienvenida
        mostrar_bienvenida(root)
    elif pantalla == 'crear_registro':
        from crear_registro import mostrar_crear_registro
        mostrar_crear_registro(root)
    elif pantalla == 'ver_registro':
        from ver_registro import mostrar_ver_registro
        mostrar_ver_registro(root, *args)  # args contiene el registro seleccionado
    elif pantalla == 'mayores':
        from mayores import mostrar_mayores
        mostrar_mayores(root, *args)  # args contiene el registro para mostrar mayores
    elif pantalla == 'situacion_financiera':
        from situacion_financiera import mostrar_situacion_financiera
        mostrar_situacion_financiera(root, *args)  # args contiene el registro para mostrar estados financieros
    elif pantalla == 'estado_resultados':
        from Estado_Resultados import abrir_estado_resultados
        abrir_estado_resultados(root, *args)
    elif pantalla == 'balanza_comprobacion':
        from balanza_comprobacion import generar_balanza
        generar_balanza(root, *args)
