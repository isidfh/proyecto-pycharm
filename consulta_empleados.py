import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import conectar


# Consultar un empleado por su matrícula
def obtener_empleado_por_matricula():
    matricula = introduce_matricula.get().strip()  # Obtener la matrícula desde el campo de texto y eliminar espacios

    if not matricula:
        messagebox.showwarning("Entrada vacía", "Por favor, ingresa una matrícula de empleado.")
        introduce_matricula.delete(0, tk.END)  # Borra el contenido del Entry
        return

    # Validar que la matrícula sea un texto válido
    if not matricula.isalnum():
        messagebox.showwarning("Entrada inválida", "La matrícula debe ser alfanumérica.")
        introduce_matricula.delete(0, tk.END)  # Borra el contenido si la entrada es inválida
        return

    conn, cursor = conectar()

    if not conn or not cursor:
        return

    # Consulta SQL para buscar un empleado por su matrícula
    consulta = """SELECT matricula, nombre_empleado, apellido1_empleado, apellido2_empleado, telefono1_empleado 
    FROM empleados 
    WHERE matricula = ?"""
    try:
        cursor.execute(consulta, (matricula,))
        # Recuperamos la primera fila que coincida con la matrícula
        fila = cursor.fetchone()

        if fila:
            # Extraer los datos
            matricula, nombre, apellido1, apellido2, telefono = fila

            # Limpiar el Treeview antes de agregar el nuevo resultado
            treeview_empleados.delete(*treeview_empleados.get_children())
            # Añadir el empleado encontrado al Treeview
            treeview_empleados.insert("", tk.END, values=(matricula, nombre, apellido1, apellido2, telefono))

        else:
            # Si no encontramos el empleado, mostrar un mensaje de advertencia
            messagebox.showinfo("Resultado de la consulta", "⚠️ Empleado no encontrado.")

            # Limpiar el contenido del TextBox
            introduce_matricula.delete(0, tk.END)  # Borrar la matrícula introducida

    except Exception as e:
        messagebox.showerror("Error en la consulta", f"Ocurrió un error al realizar la consulta:\n{str(e)}")

    # Cerrar la conexión
    conn.close()


# Mostrar todos los empleados
def mostrar_todos_los_empleados():
    introduce_matricula.delete(0, tk.END)
    conn, cursor = conectar()

    # Consulta SQL para obtener todos los empleados
    consulta = "SELECT matricula, nombre_empleado, apellido1_empleado, apellido2_empleado, telefono1_empleado FROM empleados"
    cursor.execute(consulta)

    # Recuperar todos los registros
    empleados = cursor.fetchall()

    # Limpiar el Treeview antes de agregar los nuevos resultados
    for row in treeview_empleados.get_children():
        treeview_empleados.delete(row)

    if empleados:
        # Mostrar cada empleado en el Treeview
        for empleado in empleados:
            matricula, nombre, apellido1, apellido2, telefono = empleado
            treeview_empleados.insert("", tk.END, values=(matricula, nombre, apellido1, apellido2, telefono))
    else:
        # Si no hay empleados
        treeview_empleados.insert("", tk.END, values=("No hay empleados registrados.", "", "", "", ""))

    # Cerrar la conexión
    conn.close()


# Crear la ventana principal
root = tk.Tk()
root.title("Consulta de Empleados")
root.geometry("800x600")  # Ajustar tamaño de la ventana

# Crear widgets para la consulta por matrícula
label_id_empleado = tk.Label(root, text="Matrícula de Empleado:", font=("Arial", 12))
label_id_empleado.pack(pady=5)

introduce_matricula = tk.Entry(root, font=("Arial", 12))
introduce_matricula.pack(pady=5)

consulta_button = tk.Button(root, text="Consultar", command=obtener_empleado_por_matricula, font=("Arial", 12))
consulta_button.pack(pady=10)

# Crear widgets para la tabla de empleados
label_empleados = tk.Label(root, text="Lista de Empleados", font=("Arial", 14))
label_empleados.pack(pady=10)

# Crear un Treeview para mostrar los empleados
columns = ("Matrícula", "Nombre", "Apellido1", "Apellido2", "Teléfono")
treeview_empleados = ttk.Treeview(root, columns=columns, show="headings", height=15)

# Configurar las columnas
for col in columns:
    treeview_empleados.heading(col, text=col)
    treeview_empleados.column(col, width=150, anchor="center")

treeview_empleados.pack(pady=10)

# Botón para mostrar todos los empleados
mostrar_button = tk.Button(root, text="Mostrar Todos", command=mostrar_todos_los_empleados, font=("Arial", 12))
mostrar_button.pack(pady=10)

# Ejecutar la ventana
root.mainloop()
