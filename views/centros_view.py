import tkinter as tk
from tkinter import ttk, messagebox
from database import insertar_centro, obtener_centros, eliminar_centro

class CentrosView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style="TFrame")
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        # Colores modernos (Paleta Azul/Gris oscuro)
        style.configure("Card.TFrame", background="white", relief="flat")
        style.configure("Modern.TLabel", background="white", font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="white", font=("Segoe UI", 16, "bold"), foreground="#2c3e50")
        
        # Botón estilo "Primary"
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), padding=10)
        style.map("Primary.TButton",
                  background=[('active', '#2980b9')],
                  foreground=[('active', 'white')])

    def setup_ui(self):
        # Contenedor principal con fondo gris claro para resaltar el "Card"
        self.main_container = tk.Frame(self, bg="#f5f6fa")
        self.main_container.pack(expand=True, fill="both")

        # --- HEADER ---
        header = tk.Frame(self.main_container, bg="white", height=70)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        ttk.Label(header, text="🏛️ Gestión de Instituciones", style="Title.TLabel").pack(side="left", padx=30, pady=15)

        # --- CUERPO (Contenedor con margen) ---
        body = tk.Frame(self.main_container, bg="#f5f6fa")
        body.pack(expand=True, fill="both", padx=40, pady=20)

        # SECCIÓN IZQUIERDA: FORMULARIO (Estilo Card)
        form_card = tk.Frame(body, bg="white", highlightbackground="#dcdde1", highlightthickness=1)
        form_card.place(relx=0, rely=0, relwidth=0.35, relheight=0.5)

        tk.Label(form_card, text="Registrar Nueva Sede", bg="white", font=("Segoe UI", 12, "bold"), fg="#34495e").pack(pady=(20, 10))
        
        # Campos de entrada
        input_group = tk.Frame(form_card, bg="white")
        input_group.pack(padx=30, pady=10, fill="x")

        tk.Label(input_group, text="Nombre de la Sede", bg="white", font=("Segoe UI", 9), fg="#7f8c8d").pack(anchor="w")
        self.ent_nombre = tk.Entry(input_group, font=("Segoe UI", 11), relief="flat", bg="#f1f2f6", highlightthickness=1, highlightbackground="#dcdde1")
        self.ent_nombre.pack(fill="x", pady=(5, 15), ipady=5)

        tk.Label(input_group, text="Universidad / Institución", bg="white", font=("Segoe UI", 9), fg="#7f8c8d").pack(anchor="w")
        self.ent_univ = tk.Entry(input_group, font=("Segoe UI", 11), relief="flat", bg="#f1f2f6", highlightthickness=1, highlightbackground="#dcdde1")
        self.ent_univ.pack(fill="x", pady=(5, 15), ipady=5)

        btn_save = tk.Button(form_card, text="GUARDAR CENTRO", bg="#3498db", fg="white", font=("Segoe UI", 10, "bold"), 
                             relief="flat", cursor="hand2", command=self.guardar_datos)
        btn_save.pack(fill="x", padx=30, pady=10)

        # SECCIÓN DERECHA: TABLA
        table_frame = tk.Frame(body, bg="white", highlightbackground="#dcdde1", highlightthickness=1)
        table_frame.place(relx=0.38, rely=0, relwidth=0.62, relheight=1)

        # Estilo para la tabla
        table_style = ttk.Style()
        table_style.configure("Treeview", font=("Segoe UI", 10), rowheight=35, fieldbackground="white")
        table_style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

       # --- CONFIGURACIÓN DE COLUMNAS (Centradas) ---
        self.tabla = ttk.Treeview(table_frame, columns=("ID", "Nombre", "Institución"), show="headings", selectmode="browse")
        
        # Definir encabezados
        self.tabla.heading("ID", text="ID")
        self.tabla.heading("Nombre", text="SEDE / CENTRO")
        self.tabla.heading("Institución", text="UNIVERSIDAD")
        
        # Configurar alineación central y ancho
        # anchor="center" es la clave para centrar el contenido de las celdas
        self.tabla.column("ID", width=70, anchor="center")
        self.tabla.column("Nombre", width=250, anchor="center")
        self.tabla.column("Institución", width=250, anchor="center")

        self.tabla.pack(expand=True, fill="both", padx=15, pady=15)

        # Acciones de tabla
        actions = tk.Frame(table_frame, bg="white")
        actions.pack(fill="x", side="bottom", pady=15)
        
        tk.Button(actions, text="🗑️ ELIMINAR SELECCIONADO", bg="#e74c3c", fg="white", font=("Segoe UI", 9, "bold"), 
                  relief="flat", padx=15, pady=8, command=self.eliminar_datos).pack(side="right", padx=20)

        self.cargar_datos()

    # --- Los métodos guardar_datos, eliminar_datos y cargar_datos se mantienen igual que la versión anterior ---
    def cargar_datos(self):
        for item in self.tabla.get_children(): self.tabla.delete(item)
        for fila in obtener_centros(): self.tabla.insert("", tk.END, values=fila)

    def guardar_datos(self):
        nom, uni = self.ent_nombre.get().strip(), self.ent_univ.get().strip()
        if nom and uni:
            insertar_centro(nom, uni)
            self.ent_nombre.delete(0, tk.END); self.ent_univ.delete(0, tk.END)
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Centro guardado correctamente")
        else:
            messagebox.showwarning("Error", "Completa todos los campos")

    def eliminar_datos(self):
        seleccion = self.tabla.selection()
        if seleccion:
            id_centro = self.tabla.item(seleccion)['values'][0]
            if messagebox.askyesno("Confirmar", "¿Eliminar este registro?"):
                eliminar_centro(id_centro)
                self.cargar_datos()