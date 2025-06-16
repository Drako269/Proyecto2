# gui.py

import tkinter as tk
from tkinter import messagebox
import hosts_manager
import config

class BlockerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(config.APP_NAME)
        self.root.geometry(config.WINDOW_SIZE)
        self.root.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        label_title = tk.Label(self.root, text=config.APP_NAME, font=("Arial", 14))
        label_title.pack(pady=10)

        label_instruction = tk.Label(self.root, text="Ingresa el dominio (ejemplo.com):")
        label_instruction.pack()

        self.entry_website = tk.Entry(self.root, width=30)
        self.entry_website.pack(pady=5)

        btn_block = tk.Button(self.root, text="Bloquear Sitio", width=20, command=self.handle_block)
        btn_block.pack(pady=5)

        btn_unblock = tk.Button(self.root, text="Desbloquear Sitio", width=20, command=self.handle_unblock)
        btn_unblock.pack(pady=5)

        btn_exit = tk.Button(self.root, text="Salir", width=20, command=self.root.quit)
        btn_exit.pack(pady=5)

    def handle_block(self):
        website = self.entry_website.get().strip()
        if not website:
            messagebox.showerror("Error", "Por favor ingresa un nombre de dominio.")
            return
        if hosts_manager.block_website(website):
            messagebox.showinfo("Éxito", f"Sitio '{website}' bloqueado correctamente.")
        else:
            messagebox.showwarning("Advertencia", f"El sitio '{website}' ya está bloqueado.")

    def handle_unblock(self):
        website = self.entry_website.get().strip()
        if not website:
            messagebox.showerror("Error", "Por favor ingresa un nombre de dominio.")
            return
        if hosts_manager.unblock_website(website):
            messagebox.showinfo("Éxito", f"Sitio '{website}' desbloqueado correctamente.")
        else:
            messagebox.showwarning("Advertencia", f"El sitio '{website}' no estaba bloqueado.")