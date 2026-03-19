import tkinter as tk
from tkinter import ttk, messagebox # Agregamos messagebox
import os 
from database import inicializar_db
from views.home_view import HomeView
from views.login_view import LoginView
from views.configuracion_view import ConfiguracionView

class AppAsistencia:
    def __init__(self, root):
        # 1. Inicialización de base de datos
        inicializar_db()
        
        self.root = root
        self.root.title("SPAE - Tafael Teach Edition")
        
        # --- PROTOCOLO DE CIERRE ---
        # Interceptamos el botón "X" de la ventana principal
        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_salida)
        
        # --- CONFIGURACIÓN DEL ICONO PNG ---
        ruta_icono = os.path.join(os.path.dirname(__file__), 'assets', 'asistencia.png')
        
        try:
            self.icono_app = tk.PhotoImage(file=ruta_icono)
            self.root.wm_iconphoto(True, self.icono_app)
        except Exception as e:
            print(f"Error: No se encontró el icono: {e}")
        
        # --- CONFIGURACIÓN DE GEOMETRÍA ---
        self.root.minsize(1024, 720) 
        self.root.state('zoomed')
        self.root.configure(bg="#f1f2f6") 

        # --- 2. Variables de Sesión ---
        self.usuario_id = None
        self.usuario_nombre = None
        self.docente_actual = "" 

        # --- 3. Lanzar el Login ---
        self.root.withdraw()
        self.mostrar_login()

    # =========================================================================
    # MÉTODOS DE LA CLASE
    # =========================================================================

    def confirmar_salida(self):
        """Muestra un cuadro de diálogo antes de cerrar la aplicación"""
        valor = messagebox.askquestion("Salir", "¿Está seguro que desea cerrar el sistema SPAE?", icon='warning')
        if valor == 'yes':
            self.root.destroy() # Cierra la aplicación de forma segura

    def mostrar_login(self):
        self.login_window = LoginView(self.root, self.login_exitoso)

    def login_exitoso(self, id_u, nombre):
        self.usuario_id = id_u
        self.usuario_nombre = nombre
        self.docente_actual = nombre 
        
        self.root.deiconify()
        self.root.title(f"SPAE - Sesión Activa: {self.usuario_nombre}")
        
        self.buttons = {}
        self.current_tab = None
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz principal"""
        self.navbar = tk.Frame(self.root, bg="#1e272e", height=70)
        self.navbar.pack(fill="x", side="top")
        self.navbar.pack_propagate(False)

        btn_logo = tk.Button(self.navbar, text="SPAE | Rafael Teach", 
                            fg="#dcdde1", bg="#1e272e", 
                            font=("Segoe UI", 14, "bold"), padx=30,
                            relief="flat", activebackground="#1e272e", 
                            activeforeground="white", cursor="hand2",
                            command=lambda: self.switch_tab("home"))
        btn_logo.pack(side="left")

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

        user_info = tk.Frame(self.navbar, bg="#1e272e")
        user_info.pack(side="right", padx=30, pady=15)
        tk.Label(user_info, text=f"👤 {self.usuario_nombre}", 
                 bg="#1e272e", fg="#ecf0f1", font=("Segoe UI", 10, "bold")).pack()

        self.content_area = tk.Frame(self.root, bg="#f1f2f6")
        self.content_area.pack(expand=True, fill="both")

        self.switch_tab("home")

    def switch_tab(self, key):
        if self.current_tab in self.buttons:
            self.buttons[self.current_tab].configure(fg="#95a5a6", bg="#1e272e")

        for widget in self.content_area.winfo_children():
            widget.destroy()

        self.current_tab = key
        if key in self.buttons:
            self.buttons[key].configure(fg="white", bg="#2f3640")

        if key == "home":
            view = HomeView(self.content_area, self.docente_actual)
            view.pack(expand=True, fill="both")
        elif key == "config":
            view = ConfiguracionView(self.content_area, self.usuario_id)
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