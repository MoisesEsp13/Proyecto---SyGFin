import psycopg2
from conexion import conectar_db


def guardar_transaccion(regId, cuentaId, monto, isAumento, fecha):
    conn = conectar_db()
    cursor = conn.cursor()
    query = '''INSERT INTO public.transacciones(
	        "Tran_RegId", "Tran_CuentaId", "Tran_Monto", "Tran_IsAumento", "Tran_Fecha")
	        VALUES (%s, %s, %s, %s, %s)'''
    cursor.execute(query, (regId, cuentaId, monto, isAumento, fecha))
    print("Guardado correctamente")
    conn.commit()
    conn.close()