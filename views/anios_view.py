import tkinter as tk
from tkinter import ttk, messagebox
import database
from datetime import datetime

class AniosLectivosView(ttk.Frame):
    def __init__(self, parent, usuario_id):
        super().__init__(parent)
        self.usuario_id = usuario_id
        self.edit_id = None
        
        # Obtener rol para visualización de auditoría
        self.rol_usuario = database.obtener_rol_usuario(self.usuario_id)
        
        self.setup_ui()

    def setup_ui(self):
        self.main_container = tk.Frame(self, bg="#f5f6fa")
        self.main_container.pack(expand=True, fill="both")

        # --- HEADER ---
        header = tk.Frame(self.main_container, bg="white", height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        tk.Label(header, text="📅 Gestión de Años Lectivos / Ciclos", 
                 bg="white", font=("Segoe UI", 14, "bold"), fg="#2c3e50").pack(side="left", padx=30)

        body = tk.Frame(self.main_container, bg="#f5f6fa")
        body.pack(expand=True, fill="both", padx=40, pady=20)

        # --- FORMULARIO IZQUIERDO ---
        self.form_card = tk.Frame(body, bg="white", highlightbackground="#dcdde1", highlightthickness=1)
        self.form_card.place(relx=0, rely=0, relwidth=0.30, relheight=0.45)

        self.lbl_titulo_form = tk.Label(self.form_card, text="Nuevo Año Lectivo", bg="white", 
                                        font=("Segoe UI", 12, "bold"), fg="#34495e")
        self.lbl_titulo_form.pack(pady=(20, 10))
        
        input_group = tk.Frame(self.form_card, bg="white")
        input_group.pack(padx=30, pady=10, fill="x")

        tk.Label(input_group, text="Etiqueta del Año (Ej: 2026) *", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        
        # --- VALIDACIÓN EN TIEMPO REAL ---
        vcmd = (self.register(self.solo_numeros), '%P', '%S')
        
        self.ent_etiqueta = tk.Entry(input_group, font=("Segoe UI", 11), bg="#f1f2f6", 
                                   relief="flat", highlightthickness=1,
                                   validate="key", validatecommand=vcmd)
        self.ent_etiqueta.pack(fill="x", pady=(5, 15), ipady=5)

        self.btn_save = tk.Button(self.form_card, text="GUARDAR REGISTRO", bg="#27ae60", fg="white", 
                                  font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", 
                                  command=self.guardar_datos)
        self.btn_save.pack(fill="x", padx=30, pady=5)

        self.btn_cancel = tk.Button(self.form_card, text="CANCELAR", bg="#95a5a6", fg="white", 
                                    font=("Segoe UI", 10), relief="flat", cursor="hand2", 
                                    command=self.limpiar_formulario)

        # --- SECCIÓN DERECHA: DATAGRID ---
        table_container = tk.Frame(body, bg="white", highlightbackground="#dcdde1", highlightthickness=1)
        table_container.place(relx=0.32, rely=0, relwidth=0.68, relheight=1)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, borderwidth=0)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#dcdde1")

        columnas = ("ID", "Etiqueta", "Vigencia", "Estado")
        display_cols = ["Etiqueta", "Vigencia", "Estado"]
        
        if self.rol_usuario == "Creador":
            columnas += ("CreadoEn", "CreadoPor", "ModEn", "ModPor")
            display_cols += ["CreadoEn", "CreadoPor", "ModEn", "ModPor"]

        self.tabla = ttk.Treeview(table_container, columns=columnas, show="headings", displaycolumns=display_cols)
        
        scroll_y = ttk.Scrollbar(table_container, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)

        titulos = {"Etiqueta": "AÑO LECTIVO", "Vigencia": "VIGENCIA", "Estado": "ESTADO",
                   "CreadoEn": "FECHA CREACIÓN", "CreadoPor": "AUTOR", "ModEn": "MODIFICADO", "ModPor": "POR"}
        
        for col in display_cols:
            self.tabla.heading(col, text=titulos.get(col, col))
            self.tabla.column(col, width=120, anchor="center")

        scroll_y.pack(side="right", fill="y")
        self.tabla.pack(expand=True, fill="both") 

        # --- BOTONES DE ACCIÓN ---
        actions = tk.Frame(table_container, bg="white")
        actions.pack(fill="x", side="bottom", pady=(10, 20), padx=15)

        tk.Button(actions, text="✏️ EDITAR", bg="#f39c12", fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=20, pady=8, command=self.preparar_edicion).pack(side="left", padx=(0, 10))

        tk.Button(actions, text="🚫 DESACTIVAR", bg="#e74c3c", fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=20, pady=8, command=self.eliminar_datos).pack(side="left", padx=10)

        tk.Button(actions, text="✅ ACTIVAR", bg="#2980b9", fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=20, pady=8, command=self.activar_registro).pack(side="left", padx=10)
        
        tk.Button(actions, text="📌 ESTABLECER ACTUAL", bg="#2c3e50", fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=20, pady=8, command=self.marcar_como_actual).pack(side="left", padx=10)

        self.tabla.tag_configure('desactivado', background='#fab1a0', foreground='#636e72')
        self.cargar_datos()

    def solo_numeros(self, P, S):
        if P == "": return True 
        if S.isdigit():
            return len(P) <= 4
        else:
            messagebox.showwarning("Formato Incorrecto", "Únicamente se permiten números en este campo.")
            return False

    def cargar_datos(self):
        for item in self.tabla.get_children(): self.tabla.delete(item)
        for fila in database.obtener_todos_anios():
            datos_fila = list(fila)
            datos_fila[2] = "ACTUAL" if fila[2] == 1 else "ANTERIOR"
            datos_fila[3] = "ACTIVO" if fila[3] == 1 else "DESACTIVADO"
            tag = '' if fila[3] == 1 else 'desactivado'
            self.tabla.insert("", tk.END, values=datos_fila, tags=(tag,))

    def guardar_datos(self):
        etiq = self.ent_etiqueta.get().strip()
        
        if not etiq:
            messagebox.showwarning("Atención", "Ingrese la etiqueta del año.")
            self.ent_etiqueta.focus()
            return

        if len(etiq) != 4:
            messagebox.showerror("Error", "Use 4 dígitos (Ej: 2026).")
            return

        anio_ingresado = int(etiq)
        anio_actual = datetime.now().year

        if anio_ingresado > anio_actual:
            messagebox.showerror("Año Inválido", f"No se permite registrar años futuros.\nAño máximo permitido: {anio_actual}")
            return

        if anio_ingresado < 2000:
            messagebox.showerror("Año Inválido", "El año ingresado es demasiado antiguo.")
            return

        # --- VALIDACIÓN DE DUPLICADOS CONTRA BASE DE DATOS ---
        if database.verificar_duplicado_anio(etiq, self.edit_id):
            messagebox.showerror("Error de Duplicidad", f"El año lectivo {etiq} ya existe en el sistema.\nNo se permiten registros repetidos.")
            self.ent_etiqueta.focus()
            return

        try:
            if self.edit_id is None:
                database.insertar_anio(etiq, self.usuario_id)
                messagebox.showinfo("Éxito", "Año Lectivo registrado.")
            else:
                database.actualizar_anio(self.edit_id, etiq, self.usuario_id)
                messagebox.showinfo("Éxito", "Registro actualizado.")
            
            self.limpiar_formulario()
            self.cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def preparar_edicion(self):
        sel = self.tabla.selection()
        if not sel: 
            messagebox.showwarning("Atención", "Seleccione un registro.")
            return
        valores = self.tabla.item(sel)['values']
        self.edit_id = valores[0]
        self.ent_etiqueta.delete(0, tk.END)
        self.ent_etiqueta.insert(0, valores[1])
        self.lbl_titulo_form.config(text="Editando Año", fg="#f39c12")
        self.btn_save.config(text="ACTUALIZAR", bg="#f39c12")
        self.btn_cancel.pack(fill="x", padx=30, pady=5)

    def eliminar_datos(self):
        sel = self.tabla.selection()
        if not sel: return
        valores = self.tabla.item(sel)['values']
        if valores[3] == "DESACTIVADO": return
        if messagebox.askyesno("Confirmar", f"¿Desea desactivar el año {valores[1]}?"):
            database.desactivar_anio(valores[0], self.usuario_id)
            self.cargar_datos()

    def activar_registro(self):
        sel = self.tabla.selection()
        if not sel: return
        valores = self.tabla.item(sel)['values']
        if valores[3] == "ACTIVO": return
        if messagebox.askyesno("Confirmar", f"¿Desea reactivar el año {valores[1]}?"):
            database.activar_anio(valores[0], self.usuario_id)
            self.cargar_datos()

    def marcar_como_actual(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione el año.")
            return
        valores = self.tabla.item(sel)['values']
        if valores[3] == "DESACTIVADO":
            messagebox.showerror("Error", "No se puede establecer como actual un año desactivado.")
            return
        if messagebox.askyesno("Vigencia", f"¿Establecer {valores[1]} como el año lectivo actual?"):
            database.establecer_anio_actual(valores[0], self.usuario_id)
            self.cargar_datos()

    def limpiar_formulario(self):
        self.edit_id = None
        self.ent_etiqueta.delete(0, tk.END)
        self.lbl_titulo_form.config(text="Nuevo Año Lectivo", fg="#34495e")
        self.btn_save.config(text="GUARDAR REGISTRO", bg="#27ae60")
        self.btn_cancel.pack_forget()