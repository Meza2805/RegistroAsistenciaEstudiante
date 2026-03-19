import tkinter as tk
from tkinter import ttk

class HomeView(tk.Frame):
    def __init__(self, parent, docente_nombre):
        super().__init__(parent, bg="#f1f2f6") # Fondo gris suave institucional
        self.docente = docente_nombre
        self.setup_ui()

    def setup_ui(self):
        # --- CARD DE BIENVENIDA ---
        card_welcome = tk.Frame(self, bg="white", highlightbackground="#dcdde1", highlightthickness=1)
        card_welcome.pack(padx=50, pady=(50, 20), fill="x")

        # Texto de Bienvenida
        tk.Label(card_welcome, text=f"¡Bienvenido, Prof. {self.docente}!", 
                 font=("Segoe UI", 20, "bold"), bg="white", fg="#1e272e").pack(pady=(30, 10), padx=40, anchor="w")
        
        tk.Label(card_welcome, text="Sistema Profesional de Asistencia Estudiantil (SPAE)", 
                 font=("Segoe UI", 12), bg="white", fg="#3498db").pack(padx=40, anchor="w")
        
        line = tk.Frame(card_welcome, bg="#f1f2f6", height=2)
        line.pack(fill="x", padx=40, pady=20)

        # --- DESCRIPCIÓN Y FUNCIONALIDAD ---
        info_frame = tk.Frame(card_welcome, bg="white")
        info_frame.pack(fill="x", padx=40, pady=(0, 30))

        desc_text = (
            "SPAE es una herramienta integral diseñada para optimizar el control de asistencia "
            "en entornos académicos diversos. Permite gestionar múltiples centros educativos, "
            "facultades y grupos con una estructura organizada y profesional."
        )
        
        tk.Label(info_frame, text="Descripción del Sistema:", font=("Segoe UI", 11, "bold"), 
                 bg="white", fg="#2f3640").pack(anchor="w", pady=(10, 5))
        
        lbl_desc = tk.Label(info_frame, text=desc_text, font=("Segoe UI", 10), 
                            bg="white", fg="#7f8c8d", wraplength=800, justify="left")
        lbl_desc.pack(anchor="w")

        # --- GRID DE FUNCIONALIDADES (Iconos simulados) ---
        func_container = tk.Frame(self, bg="#f1f2f6")
        func_container.pack(fill="x", padx=50, pady=20)

        # Definimos las funcionalidades clave
        features = [
            ("🏛️ Multicentro", "Gestión de carnés únicos por institución."),
            ("📊 Reportes Pro", "Exportación directa a Excel con formato oficial."),
            ("🏫 Control Total", "Manejo de horarios, aulas y grupos."),
            ("👥 Estudiantes", "Ficha técnica completa y seguimiento.")
        ]

        for i, (titulo, desc) in enumerate(features):
            f_card = tk.Frame(func_container, bg="white", highlightbackground="#dcdde1", highlightthickness=1)
            f_card.grid(row=0, column=i, padx=10, sticky="nsew")
            func_container.grid_columnconfigure(i, weight=1)

            tk.Label(f_card, text=titulo, font=("Segoe UI", 11, "bold"), bg="white", fg="#1e272e").pack(pady=(15, 5))
            tk.Label(f_card, text=desc, font=("Segoe UI", 9), bg="white", fg="#7f8c8d", wraplength=150).pack(pady=(0, 15))