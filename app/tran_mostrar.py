import psycopg2
from conexion import conectar_db


def obtener_cuentas():
    conn = conectar_db()
    cursor = conn.cursor()
    query = '''SELECT "Cuenta_Id", "Cuenta_Nom" FROM cuentas'''
    cursor.execute(query)
    cuentas = cursor.fetchall()
    conn.close()
    return cuentas