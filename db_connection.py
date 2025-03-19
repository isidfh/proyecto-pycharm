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


def obtener_empleado_por_matricula(matricula):
    conn, cursor = conectar()
    if conn is None:
        return None

    # Consulta para obtener el empleado
    consulta = "SELECT matricula, nombre_empleado, apellido1_empleado, apellido2_empleado, telefono1_empleado FROM empleados WHERE matricula = ?"
    cursor.execute(consulta, (matricula,))

    empleado = cursor.fetchone()  # Recuperar un solo registro
    conn.close()

    return empleado


# Nueva función para obtener todos los empleados
def obtener_todos_empleados():
    conn, cursor = conectar()
    if conn is None:
        return None

    # Consulta para obtener todos los empleados
    consulta = "SELECT matricula, nombre_empleado, apellido1_empleado, apellido2_empleado, telefono1_empleado FROM empleados"
    cursor.execute(consulta)

    empleados = cursor.fetchall()  # Obtener todos los registros
    conn.close()

    return empleados
