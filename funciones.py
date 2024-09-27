import psycopg2

def conectar_db():
    try:
        conn = psycopg2.connect(dbname="postgres", user="postgres",
                            password="123456", host="localhost", port="5432")
        return conn
    except:
        print("Error al conectar a la base de datos") 


def save_new_student(name, age, address):
    conn = conectar_db()
    cursor = conn.cursor()
    query = '''INSERT INTO students(name, age, address) VALUES (%s, %s, %s)'''
    cursor.execute(query, (name, age, address))
    print("Successfully inserted data")
    conn.commit()
    conn.close()


def search_student(id):
    conn = conectar_db()    
    cursor = conn.cursor()
    query = '''SELECT * FROM students WHERE id=%s'''
    cursor.execute(query, (id,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()
    return row


def get_all_students():
    conn = conectar_db()
    cursor = conn.cursor()
    query = '''SELECT * FROM students'''
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows
