import tkinter as tk
from views.centros_view import CentrosView

class ConfiguracionView(tk.Frame):
    def __init__(self, parent, usuario_id):
        super().__init__(parent, bg="white")
        self.usuario_id = usuario_id
        self.buttons = {}
        self.menu_expandido = True # Estado inicial del menú

        # --- SIDEBAR DINÁMICO ---
        self.sidebar = tk.Frame(self, bg="#2f3640", width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Contenedor para el botón de colapsar (estilo superior)
        self.header_frame = tk.Frame(self.sidebar, bg="#2f3640")
        self.header_frame.pack(fill="x", pady=(10, 20))

        # Botón Hamburguesa ☰
        self.btn_toggle = tk.Button(self.header_frame, text="☰", font=("Segoe UI", 12, "bold"),
                                   bg="#2f3640", fg="white", relief="flat", cursor="hand2",
                                   activebackground="#353b48", activeforeground="white",
                                   command=self.toggle_menu)
        self.btn_toggle.pack(side="right", padx=10)

        # Label del título (se ocultará al contraer)
        self.lbl_titulo = tk.Label(self.header_frame, text=" CONFIGURACIÓN", 
                                  font=("Segoe UI", 9, "bold"), bg="#2f3640", fg="#dcdde1")
        self.lbl_titulo.pack(side="left", padx=10)

        # Definición de opciones
        self.menu_options = [
            ("Sedes / Centros", "centros", "🏢", self.mostrar_centros),
            ("Años Lectivos", "anios", "📅", lambda: self.mostrar_proximamente("Años Lectivos")),
            ("Asignaturas", "materias", "📚", lambda: self.mostrar_proximamente("Asignaturas")),
            ("Turnos", "turnos", "🕒", lambda: self.mostrar_proximamente("Turnos"))
        ]

        # Creación de botones
        for text, key, icon, command in self.menu_options:
            # Guardamos el texto e icono por separado para poder manipularlos
            btn = tk.Button(self.sidebar, text=f"{icon}   {text}", font=("Segoe UI", 10),
                            relief="flat", bg="#2f3640", fg="#95a5a6",
                            anchor="w", padx=20, pady=12, cursor="hand2",
                            activebackground="#353b48", activeforeground="white",
                            command=command)
            btn.pack(fill="x")
            self.buttons[key] = {"btn": btn, "text": text, "icon": icon}

        # --- ÁREA DE TRABAJO ---
        self.work_area = tk.Frame(self, bg="white")
        self.work_area.pack(side="right", expand=True, fill="both")
        
        self.mostrar_centros()

    def toggle_menu(self):
        """Lógica para contraer o expandir el menú lateral"""
        if self.menu_expandido:
            # Contraer
            self.sidebar.configure(width=60)
            self.lbl_titulo.pack_forget() # Ocultar título
            for key in self.buttons:
                # Dejar solo el icono
                self.buttons[key]["btn"].configure(text=self.buttons[key]["icon"], anchor="center", padx=0)
            self.menu_expandido = False
        else:
            # Expandir
            self.sidebar.configure(width=220)
            self.lbl_titulo.pack(side="left", padx=10) # Mostrar título
            for key in self.buttons:
                # Mostrar icono + texto
                txt = self.buttons[key]["text"]
                ico = self.buttons[key]["icon"]
                self.buttons[key]["btn"].configure(text=f"{ico}   {txt}", anchor="w", padx=20)
            self.menu_expandido = True

    def actualizar_estilo_botones(self, active_key):
        for key in self.buttons:
            btn = self.buttons[key]["btn"]
            if key == active_key:
                btn.configure(bg="#353b48", fg="white")
            else:
                btn.configure(bg="#2f3640", fg="#95a5a6")

    def limpiar_area(self):
        for widget in self.work_area.winfo_children():
            widget.destroy()

    def mostrar_centros(self):
        self.actualizar_estilo_botones("centros")
        self.limpiar_area()
        view = CentrosView(self.work_area, self.usuario_id)
        view.pack(expand=True, fill="both")

    def mostrar_proximamente(self, modulo):
        claves = {"Años Lectivos": "anios", "Asignaturas": "materias", "Turnos": "turnos"}
        self.actualizar_estilo_botones(claves.get(modulo))
        self.limpiar_area()
        # ... (Mantener el label de "En desarrollo" que ya tenías)