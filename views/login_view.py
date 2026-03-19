import tkinter as tk
from tkinter import ttk, messagebox
import database
import sys

class LoginView(tk.Toplevel):
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.on_success = on_success 
        self.title("SPAE - Inicio de Sesión")
        
        # --- CONFIGURACIÓN DE GEOMETRÍA ---
        width = 400
        height = 580 # Incrementado un poco para dar espacio al nuevo botón
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        self.configure(bg="white")
        
        # Protocolo para cuando cierran la ventana desde la "X" roja
        self.protocol("WM_DELETE_WINDOW", self.salir_sistema)
        
        self.focus_force()
        self.grab_set() 
        
        self.mostrar_pssw = False
        self.setup_ui()

    def setup_ui(self):
        # Logo o Ícono Título
        tk.Label(self, text="🔑", font=("Segoe UI", 50), bg="white").pack(pady=(40, 10))
        tk.Label(self, text="Bienvenido al Sistema", font=("Segoe UI", 16, "bold"), 
                 bg="white", fg="#2c3e50").pack()
        tk.Label(self, text="Por favor, identifíquese", font=("Segoe UI", 10), 
                 bg="white", fg="#7f8c8d").pack(pady=(0, 30))

        # Contenedor de campos
        form_frame = tk.Frame(self, bg="white", padx=40)
        form_frame.pack(fill="x")

        # --- USUARIO ---
        tk.Label(form_frame, text="Usuario", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.ent_user = tk.Entry(form_frame, font=("Segoe UI", 12), relief="flat", bg="#f1f2f6", highlightthickness=1)
        self.ent_user.config(highlightbackground="#f1f2f6", highlightcolor="#3498db")
        self.ent_user.pack(fill="x", pady=(5, 15), ipady=5)
        self.ent_user.insert(0, "RafaelTeach") 

        # --- CONTRASEÑA (ESTILO WEB) ---
        tk.Label(form_frame, text="Contraseña", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        
        pass_container = tk.Frame(form_frame, bg="#f1f2f6", highlightthickness=1)
        pass_container.config(highlightbackground="#f1f2f6", highlightcolor="#3498db")
        pass_container.pack(fill="x", pady=(5, 25))

        self.ent_pass = tk.Entry(pass_container, font=("Segoe UI", 12), relief="flat", 
                                 bg="#f1f2f6", show="●", bd=0)
        self.ent_pass.pack(side="left", fill="x", expand=True, padx=(10, 0), ipady=5)
        
        self.btn_ojo = tk.Button(pass_container, text="👁️", font=("Segoe UI", 12), 
                                 bg="#f1f2f6", relief="flat", activebackground="#f1f2f6",
                                 cursor="hand2", command=self.toggle_password, bd=0)
        self.btn_ojo.pack(side="right", padx=5)
        
        self.ent_pass.focus()

        # --- BOTONES DE ACCIÓN ---
        # Botón Entrar
        btn_login = tk.Button(self, text="INICIAR SESIÓN", bg="#3498db", fg="white", 
                                font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2",
                                command=self.intentar_login)
        btn_login.pack(fill="x", padx=40, pady=(10, 5), ipady=8)

        # Botón Cancelar/Salir
        btn_cancelar = tk.Button(self, text="SALIR DEL SISTEMA", bg="white", fg="#95a5a6", 
                                font=("Segoe UI", 9), relief="flat", cursor="hand2",
                                activebackground="white", activeforeground="#c0392b",
                                command=self.salir_sistema)
        btn_cancelar.pack(fill="x", padx=40, pady=5)

        self.bind('<Return>', lambda e: self.intentar_login())

    def toggle_password(self):
        if self.mostrar_pssw:
            self.ent_pass.config(show="●")
            self.btn_ojo.config(text="👁️")
            self.mostrar_pssw = False
        else:
            self.ent_pass.config(show="")
            self.btn_ojo.config(text="🙈")
            self.mostrar_pssw = True

    def salir_sistema(self):
        """Cierra completamente la aplicación"""
        self.master.destroy()
        sys.exit()

    def intentar_login(self):
        user = self.ent_user.get().strip()
        pssw = self.ent_pass.get().strip()

        if not user or not pssw:
            messagebox.showwarning("Atención", "Ingrese sus credenciales completas.")
            return

        resultado = database.login_usuario(user, pssw)

        if resultado:
            id_u, nombre = resultado
            messagebox.showinfo("Acceso Concedido", f"Bienvenido, {nombre}")
            self.on_success(id_u, nombre) 
            self.destroy() 
        else:
            messagebox.showerror("Error de Acceso", "Usuario o contraseña incorrectos.")
            self.ent_pass.delete(0, tk.END)
            self.ent_pass.focus()