# auth_gui.py

import tkinter as tk
from tkinter import messagebox, Frame, ttk
import db_manager


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control Parental - Inicio de Sesión")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#B3C1DC")

        # Marco principal con padding
        main_frame = tk.Frame(self.root, bg="#B3C1DC")
        main_frame.pack(pady=(40, 50))

        # Título del aplicativo
        title_label = tk.Label(
            main_frame,
            text="Control Parental",
            font=("Arial", 24, "bold"),
            bg="#B3C1DC",
            fg="#4C587D",
            
        )

        title_label.pack(pady=(80, 0))  # Espacio para separar del formulario

        # Línea divisoria opcional (solo para estilo visual)
        separator = ttk.Separator(main_frame, orient="horizontal")
        separator.pack(fill="x", pady=(10, 0))

        # Formulario de login
        form_frame = tk.Frame(main_frame, bg="#B3C1DC",)
        form_frame.pack(expand=True)

        # Campo de usuario
        tk.Label(form_frame, text="Usuario:", font=("Arial", 12), bg="#B3C1DC",).pack(anchor="w", pady=(100, 0))
        self.entry_user = tk.Entry(form_frame, width=30, font=("Arial", 12), bd=2, relief="solid")
        self.entry_user.pack(pady=(0, 15))

        # Campo de contraseña
        tk.Label(form_frame, text="Contraseña:", font=("Arial", 12), bg="#B3C1DC",).pack(anchor="w")
        self.entry_pass = tk.Entry(form_frame, show="*", font=("Arial", 12), bd=2, relief="solid", width=30)
        self.entry_pass.pack(pady=(0, 20))

        # Botón de inicio de sesión
        login_button = tk.Button(
            form_frame,
            text="Iniciar Sesión",
            command=self.login,
            bg="#788AB2",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=8
        )
        login_button.pack()

        # Centramos la ventana en la pantalla
        self.center_window()

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = 400
        height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Advertencia", "Por favor completa ambos campos.")
            return

        if db_manager.validate_user(username, password):
            self.root.destroy()
            from main import AppController
            app = AppController()
            app.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")