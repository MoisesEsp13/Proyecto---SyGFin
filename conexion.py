import psycopg2

def conectar_db():
    try:
        conn = psycopg2.connect(dbname="SistemaContable", user="postgres",
                            password="123456", host="localhost", port="5432")
        return conn
    except:
        print("Error al conectar a la base de datos") 

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

