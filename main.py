import tkinter as tk
from tkinter import ttk
from database import inicializar_db
from views.centros_view import CentrosView
from views.home_view import HomeView # Importamos la nueva vista

class AppAsistencia:
    def __init__(self, root):
        inicializar_db()
        self.root = root
        self.root.title("SPAE - Shekinah Services Edition")
        self.root.state('zoomed')
        
        # DATOS DEL DOCENTE (Configuración inicial)
        self.docente_actual = "Marvin Rafael Meza Pineda"

        # FONDO GENERAL GRIS SUAVE
        self.root.configure(bg="#f1f2f6") 

        self.buttons = {}
        self.current_tab = None
        self.setup_ui()

    def setup_ui(self):
        # --- NAVBAR INSTITUCIONAL (Azul Oscuro Shekinah) ---
        self.navbar = tk.Frame(self.root, bg="#1e272e", height=70)
        self.navbar.pack(fill="x", side="top")
        self.navbar.pack_propagate(False)

        # Logo o Nombre de la App (Ahora es un botón que lleva al Home)
        btn_logo = tk.Button(self.navbar, text="SPAE | SHEKINAH", 
                            fg="#dcdde1", bg="#1e272e", 
                            font=("Segoe UI", 14, "bold"), padx=30,
                            relief="flat", activebackground="#1e272e", 
                            activeforeground="white", cursor="hand2",
                            command=lambda: self.switch_tab("home"))
        btn_logo.pack(side="left")

        # Contenedor de navegación
        nav_container = tk.Frame(self.navbar, bg="#1e272e")
        nav_container.pack(pady=(20, 0), padx=20, side="left")

        menu_items = [
            ("CONFIGURACIÓN", "config"),
            ("ESTUDIANTES", "estudiantes"),
            ("GRUPOS", "groups"),
            ("ASISTENCIA", "asistencia")
        ]

        for text, key in menu_items:
            btn = tk.Button(nav_container, text=text, font=("Segoe UI", 9, "bold"),
                            bg="#1e272e", fg="#95a5a6", relief="flat",
                            activebackground="#1e272e", activeforeground="white",
                            cursor="hand2", padx=15, pady=10,
                            command=lambda k=key: self.switch_tab(k))
            btn.pack(side="left")
            self.buttons[key] = btn
            
            btn.bind("<Enter>", lambda e, b=btn: self.on_hover(b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(b))

        # --- CUERPO PRINCIPAL ---
        self.content_area = tk.Frame(self.root, bg="#f1f2f6")
        self.content_area.pack(expand=True, fill="both")

        # Iniciamos en la pantalla de bienvenida por defecto
        self.switch_tab("home")

    def switch_tab(self, key):
        # Resetear estilos de botones anteriores
        if self.current_tab in self.buttons:
            self.buttons[self.current_tab].configure(fg="#95a5a6", bg="#1e272e")

        # Limpiar contenido
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Activar nuevo botón (si existe en el diccionario de botones)
        self.current_tab = key
        if key in self.buttons:
            self.buttons[key].configure(fg="white", bg="#2f3640")

        # Renderizado de vistas
        if key == "home":
            view = HomeView(self.content_area, self.docente_actual)
            view.pack(expand=True, fill="both")
        elif key == "config":
            view = CentrosView(self.content_area)
            view.pack(expand=True, fill="both")
        else:
            msg_frame = tk.Frame(self.content_area, bg="#f1f2f6")
            msg_frame.pack(expand=True)
            tk.Label(msg_frame, text=f"Módulo de {key.capitalize()} en desarrollo", 
                     bg="#f1f2f6", fg="#7f8c8d", font=("Segoe UI", 16)).pack()

    def on_hover(self, btn):
        if btn["fg"] != "white": 
            btn.configure(bg="#2c3e50", fg="#ecf0f1")

    def on_leave(self, btn):
        if btn["fg"] != "white":
            btn.configure(bg="#1e272e", fg="#95a5a6")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppAsistencia(root)
    root.mainloop()