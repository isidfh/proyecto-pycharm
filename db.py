import tkinter as tk
from tkinter import messagebox
import pyodbc

# Conexión a la base de datos
def conectar():
    db_path = r"C:\Proyectos Python\Access\bdCPD001\bdCPD001.accdb"  # Ajusta la ruta a tu base de datos
    conn = pyodbc.connect(f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path};")
    cursor = conn.cursor()
    return conn, cursor

# Consultar una estación por código
def obtener_estacion_por_codigo():
    codigo_estacion = entry_codigo.get().strip()  # Obtener el código desde el campo de texto y eliminar espacios
    if not codigo_estacion:
        messagebox.showwarning("Entrada vacía", "Por favor, ingresa un código de estación.")
        return

    conn, cursor = conectar()

    # Consulta SQL para buscar una estación por su código
    consulta = """SELECT codigo_estacion, letra_estacion, nombre_estacion 
    FROM estaciones WHERE codigo_estacion = ?"""
    cursor.execute(consulta, (codigo_estacion,))

    # Recuperamos la primera fila que coincida con el código
    estacion = cursor.fetchone()

    if estacion:
        # Extraer los datos y formatearlos
        codigo, letra, nombre = estacion
        resultado_label.config(
            text=f"📌 Estación encontrada:\n"
                 f"🔹 Código: {codigo}\n"
                 f"🔹 Letra: {letra}\n"
                 f"🔹 Nombre: {nombre}",
            fg="green"  # Color verde para indicar éxito
        )
    else:
        # Si no encontramos ninguna estación con ese código
        resultado_label.config(
            text="⚠️ Estación no encontrada.",
            fg="red"  # Color rojo para indicar error
        )

    # Cerrar la conexión
    conn.close()

# Crear la ventana principal
root = tk.Tk()
root.title("Consulta de Estaciones")
root.geometry("400x250")  # Ajustar tamaño de la ventana

# Crear widgets
label_codigo = tk.Label(root, text="Código de Estación:", font=("Arial", 12))
label_codigo.pack(pady=5)

entry_codigo = tk.Entry(root, font=("Arial", 12))
entry_codigo.pack(pady=5)

consulta_button = tk.Button(root, text="Consultar", command=obtener_estacion_por_codigo, font=("Arial", 12))
consulta_button.pack(pady=10)

resultado_label = tk.Label(root, text="Resultado de la consulta aparecerá aquí.", font=("Arial", 12), justify="left")
resultado_label.pack(pady=10)

# Ejecutar la ventana
root.mainloop()
