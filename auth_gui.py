# auth_gui.py

import tkinter as tk
from tkinter import messagebox
import db_manager

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("300x150")
        self.root.resizable(False, False)

        tk.Label(root, text="Usuario:").pack(pady=5)
        self.entry_user = tk.Entry(root)
        self.entry_user.pack()

        tk.Label(root, text="Contraseña:").pack(pady=5)
        self.entry_pass = tk.Entry(root, show="*")
        self.entry_pass.pack()

        tk.Button(root, text="Iniciar Sesión", command=self.login).pack(pady=10)

    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        if db_manager.validate_user(username, password):
            self.root.destroy()
            
            # Importación diferida para evitar ciclo
            from main import AppController  
            app = AppController()
            app.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")