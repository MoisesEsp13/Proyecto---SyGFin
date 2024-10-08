import psycopg2

def conectar_db():
    try:
        conn = psycopg2.connect(dbname="SistemaContable", user="postgres",
                                password="010960", host="localhost", port="5432")
        return conn
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
