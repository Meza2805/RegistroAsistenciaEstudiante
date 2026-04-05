import tkinter as tk
from views.centros_view import CentrosView
from views.anios_view import AniosLectivosView
from views.asignaturas_view import AsignaturasView
# 1. Importamos la nueva vista de Turnos
from views.turnos_view import TurnosView

class ConfiguracionView(tk.Frame):
    def __init__(self, parent, usuario_id):
        super().__init__(parent, bg="white")
        self.usuario_id = usuario_id
        self.buttons = {}
        self.menu_expandido = True 

        # --- SIDEBAR DINÁMICO ---
        self.sidebar = tk.Frame(self, bg="#2f3640", width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Contenedor para el botón de colapsar
        self.header_frame = tk.Frame(self.sidebar, bg="#2f3640")
        self.header_frame.pack(fill="x", pady=(10, 20))

        # Botón Hamburguesa ☰
        self.btn_toggle = tk.Button(self.header_frame, text="☰", font=("Segoe UI", 12, "bold"),
                                   bg="#2f3640", fg="white", relief="flat", cursor="hand2",
                                   activebackground="#353b48", activeforeground="white",
                                   command=self.toggle_menu)
        self.btn_toggle.pack(side="right", padx=10)

        self.lbl_titulo = tk.Label(self.header_frame, text=" CONFIGURACIÓN", 
                                  font=("Segoe UI", 9, "bold"), bg="#2f3640", fg="#dcdde1")
        self.lbl_titulo.pack(side="left", padx=10)

        # --- DEFINICIÓN DE OPCIONES ACTUALIZADA ---
        # Ahora todas las opciones principales están vinculadas a sus métodos
        self.menu_options = [
            ("Sedes / Centros", "centros", "🏢", self.mostrar_centros),
            ("Años Lectivos", "anios", "📅", self.mostrar_anios),
            ("Asignaturas", "materias", "📚", self.mostrar_asignaturas),
            ("Turnos / Horarios", "turnos", "🕒", self.mostrar_turnos) # <--- Vinculado
        ]

        # Creación dinámica de botones en el sidebar
        for text, key, icon, command in self.menu_options:
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
        
        # Vista inicial por defecto
        self.mostrar_centros()

    # =========================================================================
    # LÓGICA DE NAVEGACIÓN Y UI
    # =========================================================================

    def toggle_menu(self):
        """Contrae o expande el menú lateral"""
        if self.menu_expandido:
            self.sidebar.configure(width=60)
            self.lbl_titulo.pack_forget() 
            for key in self.buttons:
                self.buttons[key]["btn"].configure(text=self.buttons[key]["icon"], anchor="center", padx=0)
            self.menu_expandido = False
        else:
            self.sidebar.configure(width=220)
            self.lbl_titulo.pack(side="left", padx=10) 
            for key in self.buttons:
                txt = self.buttons[key]["text"]
                ico = self.buttons[key]["icon"]
                self.buttons[key]["btn"].configure(text=f"{ico}   {txt}", anchor="w", padx=20)
            self.menu_expandido = True

    def actualizar_estilo_botones(self, active_key):
        """Maneja el resaltado visual del botón activo"""
        for key in self.buttons:
            btn = self.buttons[key]["btn"]
            if key == active_key:
                btn.configure(bg="#353b48", fg="white")
            else:
                btn.configure(bg="#2f3640", fg="#95a5a6")

    def limpiar_area(self):
        """Elimina los widgets actuales para cargar una nueva vista"""
        for widget in self.work_area.winfo_children():
            widget.destroy()

    # =========================================================================
    # MÉTODOS DE RENDERIZADO DE VISTAS
    # =========================================================================

    def mostrar_centros(self):
        self.actualizar_estilo_botones("centros")
        self.limpiar_area()
        view = CentrosView(self.work_area, self.usuario_id)
        view.pack(expand=True, fill="both")

    def mostrar_anios(self):
        self.actualizar_estilo_botones("anios")
        self.limpiar_area()
        view = AniosLectivosView(self.work_area, self.usuario_id)
        view.pack(expand=True, fill="both")

    def mostrar_asignaturas(self):
        self.actualizar_estilo_botones("materias")
        self.limpiar_area()
        view = AsignaturasView(self.work_area, self.usuario_id)
        view.pack(expand=True, fill="both")

    def mostrar_turnos(self):
        """Carga la nueva vista de gestión de turnos"""
        self.actualizar_estilo_botones("turnos")
        self.limpiar_area()
        view = TurnosView(self.work_area, self.usuario_id)
        view.pack(expand=True, fill="both")

    def mostrar_proximamente(self, modulo):
        """Placeholder para módulos en desarrollo"""
        self.limpiar_area()
        tk.Label(self.work_area, text=f"Módulo de {modulo}\nEn desarrollo...", 
                 bg="white", fg="#7f8c8d", font=("Segoe UI", 14)).pack(expand=True)