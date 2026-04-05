import tkinter as tk
from tkinter import ttk, messagebox
import database
import re

class TurnosView(ttk.Frame):
    def __init__(self, parent, usuario_id):
        super().__init__(parent)
        self.usuario_id = usuario_id
        self.edit_id = None
        self.rol_usuario = database.obtener_rol_usuario(self.usuario_id)
        self.setup_ui()

    def setup_ui(self):
        self.main_container = tk.Frame(self, bg="#f5f6fa")
        self.main_container.pack(expand=True, fill="both")

        # --- HEADER ---
        header = tk.Frame(self.main_container, bg="white", height=60)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        tk.Label(header, text="🕒 Gestión de Turnos y Horarios", 
                 bg="white", font=("Segoe UI", 14, "bold"), fg="#2c3e50").pack(side="left", padx=30)

        body = tk.Frame(self.main_container, bg="#f5f6fa")
        body.pack(expand=True, fill="both", padx=40, pady=20)

        # --- FORMULARIO IZQUIERDO ---
        self.form_card = tk.Frame(body, bg="white", highlightbackground="#dcdde1", highlightthickness=1)
        self.form_card.place(relx=0, rely=0, relwidth=0.35, relheight=0.8)

        self.lbl_titulo_form = tk.Label(self.form_card, text="Configurar Turno", bg="white", 
                                        font=("Segoe UI", 12, "bold"), fg="#34495e")
        self.lbl_titulo_form.pack(pady=(20, 10))
        
        # Grupo: Nombre del Turno
        name_group = tk.Frame(self.form_card, bg="white")
        name_group.pack(padx=30, pady=5, fill="x")
        tk.Label(name_group, text="Nombre del Turno *", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_nombre = tk.Entry(name_group, font=("Segoe UI", 11), bg="#f1f2f6", relief="flat", highlightthickness=1)
        self.ent_nombre.pack(fill="x", pady=5, ipady=5)

        # Listas de valores
        horas_vals = [f"{i:02d}" for i in range(1, 13)]
        minutos_vals = [f"{i:02d}" for i in range(0, 60)]

        # --- SELECTORES DE HORA CON VALIDACIÓN AL SALIR (FocusOut) ---
        
        # Inicio
        start_group = tk.LabelFrame(self.form_card, text=" Hora de Inicio ", bg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        start_group.pack(padx=30, pady=10, fill="x")

        self.cb_h_ini = ttk.Combobox(start_group, values=horas_vals, width=5)
        self.cb_h_ini.set("08")
        self.cb_h_ini.pack(side="left", padx=2)
        self.cb_h_ini.bind("<FocusOut>", lambda e: self.validar_campo_tiempo(self.cb_h_ini, 1, 12, "Hora"))

        tk.Label(start_group, text=":", bg="white", font=("Segoe UI", 10, "bold")).pack(side="left")
        
        self.cb_m_ini = ttk.Combobox(start_group, values=minutos_vals, width=5)
        self.cb_m_ini.set("00")
        self.cb_m_ini.pack(side="left", padx=2)
        self.cb_m_ini.bind("<FocusOut>", lambda e: self.validar_campo_tiempo(self.cb_m_ini, 0, 59, "Minutos"))
        
        self.cb_p_ini = ttk.Combobox(start_group, values=["AM", "PM"], width=5, state="readonly")
        self.cb_p_ini.set("AM")
        self.cb_p_ini.pack(side="left", padx=5)

        # Fin
        end_group = tk.LabelFrame(self.form_card, text=" Hora de Finalización ", bg="white", font=("Segoe UI", 9, "bold"), padx=10, pady=10)
        end_group.pack(padx=30, pady=10, fill="x")

        self.cb_h_fin = ttk.Combobox(end_group, values=horas_vals, width=5)
        self.cb_h_fin.set("12")
        self.cb_h_fin.pack(side="left", padx=2)
        self.cb_h_fin.bind("<FocusOut>", lambda e: self.validar_campo_tiempo(self.cb_h_fin, 1, 12, "Hora"))

        tk.Label(end_group, text=":", bg="white", font=("Segoe UI", 10, "bold")).pack(side="left")
        
        self.cb_m_fin = ttk.Combobox(end_group, values=minutos_vals, width=5)
        self.cb_m_fin.set("00")
        self.cb_m_fin.pack(side="left", padx=2)
        self.cb_m_fin.bind("<FocusOut>", lambda e: self.validar_campo_tiempo(self.cb_m_fin, 0, 59, "Minutos"))
        
        self.cb_p_fin = ttk.Combobox(end_group, values=["AM", "PM"], width=5, state="readonly")
        self.cb_p_fin.set("PM")
        self.cb_p_fin.pack(side="left", padx=5)

        # Botones
        self.btn_save = tk.Button(self.form_card, text="GUARDAR TURNO", bg="#27ae60", fg="white", 
                                  font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", 
                                  command=self.guardar_datos)
        self.btn_save.pack(fill="x", padx=30, pady=(20, 5))

        self.btn_cancel = tk.Button(self.form_card, text="CANCELAR", bg="#95a5a6", fg="white", 
                                    font=("Segoe UI", 10), relief="flat", cursor="hand2", 
                                    command=self.limpiar_formulario)
        self.btn_cancel.pack_forget()

        # --- DATAGRID ---
        table_container = tk.Frame(body, bg="white", highlightbackground="#dcdde1", highlightthickness=1)
        table_container.place(relx=0.37, rely=0, relwidth=0.63, relheight=1)

        columnas = ("ID", "Nombre", "Inicio", "Fin", "Estado")
        display_cols = ["Nombre", "Inicio", "Fin", "Estado"]
        self.tabla = ttk.Treeview(table_container, columns=columnas, show="headings", displaycolumns=display_cols)
        
        for col in display_cols:
            self.tabla.heading(col, text=col.upper())
            self.tabla.column(col, width=100, anchor="center")
        self.tabla.pack(expand=True, fill="both")

        actions = tk.Frame(table_container, bg="white")
        actions.pack(fill="x", side="bottom", pady=(10, 20), padx=15)
        tk.Button(actions, text="✏️ EDITAR", bg="#f39c12", fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=20, pady=8, command=self.preparar_edicion).pack(side="left", padx=(0, 10))
        tk.Button(actions, text="🚫 DESACTIVAR", bg="#e74c3c", fg="white", font=("Segoe UI", 9, "bold"),
                  relief="flat", padx=20, pady=8, command=self.eliminar_datos).pack(side="left", padx=10)

        self.cargar_datos()

    # --- LÓGICA DE VALIDACIÓN PROACTIVA ---
    def validar_campo_tiempo(self, combo, minimo, maximo, tipo):
        valor = combo.get().strip()
        if not valor: return

        try:
            num = int(valor)
            if minimo <= num <= maximo:
                # Formateo automático: ej. "5" -> "05"
                combo.set(f"{num:02d}")
            else:
                messagebox.showerror("Rango Inválido", f"{tipo} debe estar entre {minimo:02d} y {maximo:02d}")
                combo.focus()
                combo.set(f"{minimo:02d}") # Reset al mínimo para ayudar al usuario
        except ValueError:
            messagebox.showerror("Error de Entrada", f"Ingrese un valor numérico para {tipo.lower()}")
            combo.focus()
            combo.set(f"{minimo:02d}")

    def convertir_a_24h(self, hora, minuto, periodo):
        h = int(hora)
        m = int(minuto)
        if periodo == "PM" and h < 12: h += 12
        if periodo == "AM" and h == 12: h = 0
        return h * 60 + m

    def cargar_datos(self):
        for item in self.tabla.get_children(): self.tabla.delete(item)
        for fila in database.obtener_todos_turnos():
            datos = list(fila)
            datos[4] = "ACTIVO" if fila[4] == 1 else "DESACTIVADO"
            self.tabla.insert("", tk.END, values=datos)

    def guardar_datos(self):
        nom = self.ent_nombre.get().strip().upper()
        if not nom:
            messagebox.showwarning("Atención", "Ingrese el nombre del turno."); return

        h_i, m_i, p_i = self.cb_h_ini.get(), self.cb_m_ini.get(), self.cb_p_ini.get()
        h_f, m_f, p_f = self.cb_h_fin.get(), self.cb_m_fin.get(), self.cb_p_fin.get()

        # Validación lógica final
        inicio_total = self.convertir_a_24h(h_i, m_i, p_i)
        fin_total = self.convertir_a_24h(h_f, m_f, p_f)

        if fin_total <= inicio_total:
            messagebox.showerror("Horario Ilógico", "La hora de fin debe ser posterior a la de inicio."); return

        ini_str = f"{h_i}:{m_i} {p_i}"
        fin_str = f"{h_f}:{m_f} {p_f}"

        if database.verificar_duplicado_turno(nom, ini_str, fin_str, self.edit_id):
            messagebox.showerror("Duplicado", "Ya existe este turno con el mismo horario."); return

        try:
            if self.edit_id is None:
                database.insertar_turno(nom, ini_str, fin_str, self.usuario_id)
            else:
                database.actualizar_turno(self.edit_id, nom, ini_str, fin_str, self.usuario_id)
            self.limpiar_formulario()
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Turno guardado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def preparar_edicion(self):
        sel = self.tabla.selection()
        if not sel: return
        v = self.tabla.item(sel)['values']
        self.edit_id = v[0]
        self.ent_nombre.delete(0, tk.END); self.ent_nombre.insert(0, v[1])
        
        # Parseo seguro
        try:
            h_i, rem_i = v[2].split(':'); m_i, p_i = rem_i.split(' ')
            self.cb_h_ini.set(h_i); self.cb_m_ini.set(m_i); self.cb_p_ini.set(p_i)
            h_f, rem_f = v[3].split(':'); m_f, p_f = rem_f.split(' ')
            self.cb_h_fin.set(h_f); self.cb_m_fin.set(m_f); self.cb_p_fin.set(p_f)
        except: pass

        self.lbl_titulo_form.config(text="Editando Turno", fg="#f39c12")
        self.btn_save.config(text="ACTUALIZAR TURNO", bg="#f39c12")
        self.btn_cancel.pack(fill="x", padx=30, pady=5)

    def eliminar_datos(self):
        sel = self.tabla.selection()
        if not sel: return
        v = self.tabla.item(sel)['values']
        if messagebox.askyesno("Confirmar", f"¿Desactivar turno {v[1]}?"):
            database.desactivar_turno(v[0], self.usuario_id)
            self.cargar_datos()

    def limpiar_formulario(self):
        self.edit_id = None
        self.ent_nombre.delete(0, tk.END)
        self.cb_h_ini.set("08"); self.cb_m_ini.set("00"); self.cb_p_ini.set("AM")
        self.cb_h_fin.set("12"); self.cb_m_fin.set("00"); self.cb_p_fin.set("PM")
        self.lbl_titulo_form.config(text="Nuevo Turno", fg="#34495e")
        self.btn_save.config(text="GUARDAR TURNO", bg="#27ae60")
        self.btn_cancel.pack_forget()