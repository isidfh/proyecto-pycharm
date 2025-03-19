import pyodbc

def conectar():
    try:
        db_path = r"C:\Proyectos Python\Access\bdCPD001\bdCPD001.accdb"
        conn = pyodbc.connect(f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};")
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print(f"Error de conexión a la base de datos: {db_path}, error: {e}")
        return None, None

