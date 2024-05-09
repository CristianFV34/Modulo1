# -*- coding: utf-8 -*-
import tkinter.font as tkFont
import cx_Oracle
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# Función para mostrar los datos de la tabla
def mostrar_datos():
    # Conexión a la base de datos Oracle
    conexion = cx_Oracle.connect(
        user="USUARIO_CRISTIAN",
        password="Dev99_2000",
        dsn="Cristian:1521/xe"
    )
    
    if conexion:
        # Ejecutar una consulta para obtener los datos de la tabla
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM alumnos")
        datos = cursor.fetchall()
        #print(datos)

        # Cerrar cursor y conexión
        cursor.close()
        conexion.close()

        # Mostrar los datos en una ventana nueva
        ventana_resultados = tk.Toplevel(root)
        ventana_resultados.title("Datos de la tabla")

        # Mostrar los datos en una etiqueta
        clientes_headers=("ID","Nombre","Apellido paterno","Apellido materno","Carrera","Fecha de nacimiento")
        clientes_tab = Table(ventana_resultados, title="Alumnos registrados", headers=clientes_headers)
        clientes_tab.pack()

        for row in datos:
            clientes_tab.add_row(row)
    else:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")

class Table(tk.Frame):
    def __init__(self, parent=None, title="", headers=[], height=10, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self._title = tk.Label(self, text=title, background="#ECCCCE", font=("Helvetica", 16))
        self._headers = headers
        self._tree = ttk.Treeview(self,
                                  height=height,
                                  columns=self._headers, 
                                  show="headings")
        self._title.pack(side=tk.TOP, fill="x")

        # Agregamos dos scrollbars 
        vsb = ttk.Scrollbar(self, orient="vertical", command=self._tree.yview)
        vsb.pack(side='right', fill='y')
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self._tree.xview)
        hsb.pack(side='bottom', fill='x')

        self._tree.configure(xscrollcommand=hsb.set, yscrollcommand=vsb.set)
        self._tree.pack(side="left")

        for header in self._headers:
            self._tree.heading(header, text=header.title())
            self._tree.column(header, stretch=True,
                              width=tkFont.Font().measure(header.title()))

    def add_row(self, row):
        self._tree.insert('', 'end', values=row)
        for i, item in enumerate(row):
            col_width = tkFont.Font().measure(item)
            if self._tree.column(self._headers[i], width=None) < col_width:
                    self._tree.column(self._headers[i], width=col_width)

# Crear la ventana principal
root = tk.Tk()
root.title("Mostrar Datos")
root.geometry("250x50+560+240")

# Botón para mostrar los datos
boton_mostrar = tk.Button(root, text="Mostrar", command=mostrar_datos)
boton_mostrar.pack(pady=10)

root.mainloop()
