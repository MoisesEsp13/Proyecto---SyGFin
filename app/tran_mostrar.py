import tkinter as tk
from tkinter import ttk
from tran_guardar import *
from conexion import conectar_db
from tkcalendar import DateEntry

def obtener_cuentas():
    conn = conectar_db()
    cursor = conn.cursor()
    query = '''SELECT "Cuenta_Id", "Cuenta_Nom" FROM cuentas'''
    cursor.execute(query)
    cuentas = cursor.fetchall()
    conn.close()
    return cuentas