import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import obtener_empleado_por_matricula, obtener_todos_empleados  # Importamos las funciones necesarias

# Función para consultar un empleado por matrícula
def obtener_empleado_por_matricula_ui():
    matricula = introduce_matricula.get().strip()  # Obtener la matrícula desde el campo de texto y eliminar espacios
    if not matricula:
        messagebox.showwarning("Entrada vacía", "Por favor, ingresa una matrícula de empleado.")
        introduce_matricula.delete(0, tk.END)  # Borrar el texto en el TextBox
        return

    # Validar que la matrícula sea un texto válido
    if not matricula.isalnum():
        messagebox.showwarning("Entrada inválida", "La matrícula debe ser alfanumérica.")
        introduce_matricula.delete(0, tk.END)  # Borrar el texto en el TextBox
        return

    # Llamar a la función de db_connection para obtener el empleado
    empleado = obtener_empleado_por_matricula(matricula)

    # Limpiar el Treeview antes de agregar el nuevo resultado
    treeview_empleados.delete(*treeview_empleados.get_children())

    if empleado:
        matricula, nombre, apellido1, apellido2, telefono = empleado
        treeview_empleados.insert("", tk.END, values=(matricula, nombre, apellido1, apellido2, telefono))
    else:
        messagebox.showwarning("Empleado no encontrado", "No se encontró ningún empleado con esa matrícula.")
        introduce_matricula.delete(0, tk.END)  # Borrar el texto en el TextBox


# Función para consultar todos los empleados
def consultar_todos_empleados_ui():
    # Borrar el contenido del TextBox antes de hacer la consulta
    introduce_matricula.delete(0, tk.END)

    # Limpiar el Treeview antes de agregar los resultados
    treeview_empleados.delete(*treeview_empleados.get_children())

    # Llamar a la función de db_connection para obtener todos los empleados
    empleados = obtener_todos_empleados()

    if empleados:
        for empleado in empleados:
            matricula, nombre, apellido1, apellido2, telefono = empleado
            treeview_empleados.insert("", tk.END, values=(matricula, nombre, apellido1, apellido2, telefono))
    else:
        messagebox.showwarning("No hay empleados", "No hay empleados registrados en la base de datos.")


# Crear la ventana principal
root = tk.Tk()
root.title("Consulta de Empleados")
root.geometry("800x600")  # Ajustar tamaño de la ventana

# Crear widgets para la consulta por matrícula
label_id_empleado = tk.Label(root, text="Matrícula de Empleado:", font=("Arial", 12))
label_id_empleado.pack(pady=5)

introduce_matricula = tk.Entry(root, font=("Arial", 12))
introduce_matricula.pack(pady=5)

consulta_button = tk.Button(root, text="Consultar", command=obtener_empleado_por_matricula_ui, font=("Arial", 12))
consulta_button.pack(pady=10)

# Botón para consultar todos los empleados
todos_button = tk.Button(root, text="Consultar Todos", command=consultar_todos_empleados_ui, font=("Arial", 12))
todos_button.pack(pady=10)

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

# Ejecutar la ventana
root.mainloop()
