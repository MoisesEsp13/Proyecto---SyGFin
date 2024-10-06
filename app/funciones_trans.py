import psycopg2
from conexion import conectar_db


def obtener_transacciones(reg_id):
    conn = conectar_db()
    cursor = conn.cursor()
    query = '''SELECT t."Tran_Fecha", c."Cuenta_Nom", t."Tran_MontoDeb", t."Tran_MontoCre"
               FROM transacciones t
               JOIN cuentas c ON t."Tran_CuentaId" = c."Cuenta_Id"
               WHERE t."Tran_RegId" = %s
               ORDER BY t."Tran_Fecha"'''
    cursor.execute(query, (reg_id,))
    transacciones = cursor.fetchall()
    conn.close()
    return transacciones


def obtener_tipos_cuenta():
    conn = conectar_db()
    cursor = conn.cursor()
    query = '''SELECT * FROM public.cuenta_tipos'''
    cursor.execute(query)
    tipos_cuenta = cursor.fetchall()
    conn.close()
    return tipos_cuenta


def obtener_cuentas(tipo_id):
    conn = conectar_db()
    cursor = conn.cursor()
    if tipo_id == None:
        query = '''SELECT c."Cuenta_Id", c."Cuenta_Nom" FROM cuentas c'''
        cursor.execute(query)
    else:
        query = '''SELECT c."Cuenta_Id", c."Cuenta_Nom" FROM cuentas c
                   WHERE c."Cuenta_CuentaTipoId" = %s'''
        cursor.execute(query, (tipo_id,))
    cuentas = cursor.fetchall()
    conn.close()
    return cuentas


def sincronizar_id(event, cmb_cuenta_nom, cmb_cuenta_id, cuentas):
    nombre_seleccionado = cmb_cuenta_nom.get()
    for cuenta in cuentas:
        if cuenta[1] == nombre_seleccionado:
            cmb_cuenta_id.set(cuenta[0])
            break


def sincronizar_nom(event, cmb_cuenta_nom, cmb_cuenta_id, cuentas):
    id_seleccionado = cmb_cuenta_id.get()
    for cuenta in cuentas:
        if str(cuenta[0]) == id_seleccionado:
            cmb_cuenta_nom.set(cuenta[1])
            break


def tipo_cuenta_seleccion(event, cmb_cuenta_tipo, cmb_cuenta_id, cmb_cuenta_nom, tipos_cuenta):
   
    # Limpiar los valores 
    cmb_cuenta_id.set('')
    cmb_cuenta_nom.set('')

    # Obtener el tipo de cuenta seleccionado
    seleccion = cmb_cuenta_tipo.get()
    
    if seleccion and seleccion in tipos_cuenta:
        tipo_id = tipos_cuenta[seleccion]
    else:
        tipo_id = None
    
    cuentas = obtener_cuentas(tipo_id)

    # Actualizar los comboboxes 
    cmb_cuenta_id['values'] = [cuenta[0] for cuenta in cuentas]
    cmb_cuenta_nom['values'] = [cuenta[1] for cuenta in cuentas]

    cmb_cuenta_id.bind("<<ComboboxSelected>>", lambda event: sincronizar_nom(event, cmb_cuenta_nom, cmb_cuenta_id, cuentas))
    cmb_cuenta_nom.bind("<<ComboboxSelected>>", lambda event: sincronizar_id(event, cmb_cuenta_nom, cmb_cuenta_id, cuentas))


def guardar_transaccion(regId, cuentaId, monto, isAumento, fecha):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''SELECT "Cuenta_CuentaTipoId" FROM cuentas WHERE "Cuenta_Id" = %s''', (cuentaId,))
    cuenta_tipo = cursor.fetchone()[0]

    if isAumento:
        if cuenta_tipo in [1, 2, 3, 6]:
            query = '''INSERT INTO public.transacciones(
            "Tran_RegId", "Tran_CuentaId", "Tran_MontoDeb", "Tran_Fecha")
            VALUES (%s, %s, %s, %s)'''
            cursor.execute(query, (regId, cuentaId, monto, fecha))

        else:
            query = '''INSERT INTO public.transacciones(
            "Tran_RegId", "Tran_CuentaId", "Tran_MontoCre", "Tran_Fecha")
            VALUES (%s, %s, %s, %s)'''
            cursor.execute(query, (regId, cuentaId, monto, fecha))
    
    else:
        if cuenta_tipo in [1, 2, 3, 6]:
            query = '''INSERT INTO public.transacciones(
            "Tran_RegId", "Tran_CuentaId", "Tran_MontoCre", "Tran_Fecha")
            VALUES (%s, %s, %s, %s)'''
            cursor.execute(query, (regId, cuentaId, monto, fecha))

        else:
            query = '''INSERT INTO public.transacciones(
            "Tran_RegId", "Tran_CuentaId", "Tran_MontoDeb", "Tran_Fecha")
            VALUES (%s, %s, %s, %s)'''
            cursor.execute(query, (regId, cuentaId, monto, fecha))

    print("Guardado correctamente")
    conn.commit()
    conn.close()