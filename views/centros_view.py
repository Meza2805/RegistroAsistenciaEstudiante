import tkinter as tk
from tkinter import ttk, messagebox
import database

class CentrosView(ttk.Frame):
    def __init__(self, parent, usuario_id):
        super().__init__(parent)
        self.usuario_id = usuario_id  
        self.edit_id = None           
        
        # --- OBTENER ROL DEL USUARIO (Para mostrar u ocultar auditoría) ---
        # Asumimos que database.obtener_rol(id) devuelve 'Creador' o similar
        self.rol_usuario = database.obtener_rol_usuario(self.usuario_id)
        
        self.setup_ui()

    def setup_ui(self):
        self.main_container = tk.Frame(self, bg="#f5f6fa")
        self.main_container.pack(expand=True, fill="both")

        # --- HEADER ---
        header = tk.Frame(self.main_container, bg="white", height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        tk.Label(header, text="🏛️ Gestión Maestra de Sedes e Instituciones", 
                 bg="white", font=("Segoe UI", 14, "bold"), fg="#2c3e50").pack(side="left", padx=30)

        body = tk.Frame(self.main_container, bg="#f5f6fa")
        body.pack(expand=True, fill="both", padx=40, pady=20)

        # --- FORMULARIO IZQUIERDO ---
        self.form_card = tk.Frame(body, bg="white", highlightbackground="#dcdde1", highlightthickness=1)
        self.form_card.place(relx=0, rely=0, relwidth=0.30, relheight=0.6)

        self.lbl_titulo_form = tk.Label(self.form_card, text="Datos del Centro", bg="white", 
                                        font=("Segoe UI", 12, "bold"), fg="#34495e")
        self.lbl_titulo_form.pack(pady=(20, 10))
        
        input_group = tk.Frame(self.form_card, bg="white")
        input_group.pack(padx=30, pady=10, fill="x")

        tk.Label(input_group, text="Sede *", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_nombre = tk.Entry(input_group, font=("Segoe UI", 11), bg="#f1f2f6", relief="flat", highlightthickness=1)
        self.ent_nombre.pack(fill="x", pady=(5, 15), ipady=5)

        tk.Label(input_group, text="Institución *", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_univ = tk.Entry(input_group, font=("Segoe UI", 11), bg="#f1f2f6", relief="flat", highlightthickness=1)
        self.ent_univ.pack(fill="x", pady=(5, 15), ipady=5)

        self.btn_save = tk.Button(self.form_card, text="GUARDAR REGISTRO", bg="#27ae60", fg="white", 
                                  font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", 
                                  command=self.guardar_datos)
        self.btn_save.pack(fill="x", padx=30, pady=5)

        self.btn_cancel = tk.Button(self.form_card, text="CANCELAR", bg="#95a5a6", fg="white", 
                                   font=("Segoe UI", 10), relief="flat", cursor="hand2", 
                                   command=self.limpiar_formulario)

        # --- SECCIÓN DERECHA: DATAGRID MODERNO ---
        table_container = tk.Frame(body, bg="white", highlightbackground="#dcdde1", highlightthickness=1)
        table_container.place(relx=0.32, rely=0, relwidth=0.68, relheight=1)
# --- SECCIÓN DERECHA: DATAGRID MODERNO ---
        # Cambiamos el fondo del contenedor al color que quieres para las líneas
        color_grid = "#2f3640" 
        table_container = tk.Frame(body, bg=color_grid, highlightbackground="#dcdde1", highlightthickness=1)
        table_container.place(relx=0.32, rely=0, relwidth=0.68, relheight=1)

        # Estilo del Treeview
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure("Treeview", 
                        font=("Segoe UI", 10), 
                        rowheight=30,
                        background="white",
                        fieldbackground="white",
                        foreground="#2c3e50",
                        borderwidth=0) # Quitamos el borde default

        style.map("Treeview", 
                  background=[('selected', '#3498db')],
                  foreground=[('selected', 'white')])

        style.configure("Treeview.Heading", 
                        font=("Segoe UI", 10, "bold"), 
                        background="#dcdde1", 
                        foreground="#2c3e50",
                        borderwidth=1)

        # Columnas dinámicas según rol
        columnas = ("ID", "Nombre", "Univ", "Estado")
        display_cols = ["Nombre", "Univ", "Estado"]
        
        if self.rol_usuario == "Creador":
            columnas += ("CreadoEn", "CreadoPor", "ModEn", "ModPor")
            display_cols += ["CreadoEn", "CreadoPor", "ModEn", "ModPor"]

        self.tabla = ttk.Treeview(table_container, columns=columnas, show="headings", displaycolumns=display_cols)
        
        # --- EL TRUCO PARA LAS LÍNEAS ---
        # Al empaquetar con un ipadx/ipady de 1 o simplemente con un fondo oscuro en el frame,
        # las líneas aparecerán.
        
        scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(table_container, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        titulos = {"Nombre": "SEDE / CENTRO", "Univ": "INSTITUCIÓN", "Estado": "ESTADO",
                   "CreadoEn": "FECHA CREACIÓN", "CreadoPor": "AUTOR", 
                   "ModEn": "ÚLT. MODIF.", "ModPor": "MODIF. POR"}
        
        for col in display_cols:
            self.tabla.heading(col, text=titulos.get(col, col))
            self.tabla.column(col, width=150, anchor="center")

        # Ajustamos el layout para que el fondo del frame (color_grid) se vea
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        
        # El fill="both" con el contenedor oscuro hará que el Treeview se "dibuje" encima
        # dejando ver los bordes si configuramos el espaciado
        self.tabla.pack(expand=True, fill="both", padx=0, pady=0) 

        # --- BOTONES DE ACCIÓN (Contenedor blanco para que no herede el color gris) ---
        actions = tk.Frame(table_container, bg="white")
        actions.pack(fill="x", side="bottom") # Quitamos los pady para que pegue abajo

        tk.Button(actions, text="✏️ EDITAR", bg="#f39c12", fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=15, pady=5, command=self.preparar_edicion).pack(side="left", padx=5)

        tk.Button(actions, text="🚫 DESACTIVAR", bg="#e74c3c", fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=15, pady=5, command=self.eliminar_datos).pack(side="left", padx=5)

        tk.Button(actions, text="✅ ACTIVAR", bg="#2980b9", fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=15, pady=5, command=self.activar_registro).pack(side="left", padx=5)

        # Configuración de colores para filas desactivadas
        self.tabla.tag_configure('desactivado', background='#fab1a0', foreground='#636e72')

        self.cargar_datos()

    def cargar_datos(self):
        for item in self.tabla.get_children(): self.tabla.delete(item)
        
        for fila in database.obtener_todos_centros():
            datos_fila = list(fila)
            
            # 1. Formatear el Estado para el usuario
            datos_fila[3] = "ACTIVO" if fila[3] == 1 else "DESACTIVADO"
            
            # 2. Manejar valores nulos en auditoría (Modificación)
            # Si la fecha o el usuario es None (porque nunca se ha editado)
            if datos_fila[6] is None: datos_fila[6] = "---" # Fecha mod
            if datos_fila[7] is None: datos_fila[7] = "---" # Usuario mod
            
            tag = '' if fila[3] == 1 else 'desactivado'
            self.tabla.insert("", tk.END, values=datos_fila, tags=(tag,))

    def activar_registro(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un registro desactivado.")
            return
        
        valores = self.tabla.item(sel)['values']
        if valores[3] == "ACTIVO":
            messagebox.showinfo("Info", "Este registro ya se encuentra activo.")
            return

        if messagebox.askyesno("Confirmar", f"¿Desea reactivar la sede {valores[1]}?"):
            database.activar_centro(valores[0], self.usuario_id)
            self.cargar_datos()

    def guardar_datos(self):
        nom = self.ent_nombre.get().strip()
        uni = self.ent_univ.get().strip()

        if not nom or not uni:
            messagebox.showwarning("Atención", "Complete los campos obligatorios.")
            return

        try:
            if self.edit_id is None:
                database.insertar_centro(nom, uni, self.usuario_id)
            else:
                database.actualizar_centro(self.edit_id, nom, uni, self.usuario_id)
            
            self.limpiar_formulario()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def preparar_edicion(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una fila.")
            return

        valores = self.tabla.item(sel)['values']
        self.edit_id = valores[0]
        
        self.ent_nombre.delete(0, tk.END)
        self.ent_nombre.insert(0, valores[1])
        self.ent_univ.delete(0, tk.END)
        self.ent_univ.insert(0, valores[2])

        self.lbl_titulo_form.config(text="Editando Institución", fg="#f39c12")
        self.btn_save.config(text="ACTUALIZAR DATOS", bg="#f39c12")
        self.btn_cancel.pack(fill="x", padx=30, pady=5)

    def eliminar_datos(self):
        sel = self.tabla.selection()
        if not sel: return
        
        valores = self.tabla.item(sel)['values']
        if valores[3] == "DESACTIVADO": return

        if messagebox.askyesno("Confirmar", "¿Desea desactivar esta sede?"):
            database.desactivar_centro(valores[0], self.usuario_id)
            self.cargar_datos()

    def limpiar_formulario(self):
        self.edit_id = None
        self.ent_nombre.delete(0, tk.END)
        self.ent_univ.delete(0, tk.END)
        self.lbl_titulo_form.config(text="Datos del Centro", fg="#34495e")
        self.btn_save.config(text="GUARDAR REGISTRO", bg="#27ae60")
        self.btn_cancel.pack_forget()