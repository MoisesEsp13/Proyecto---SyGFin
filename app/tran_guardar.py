import psycopg2
from conexion import conectar_db


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


    