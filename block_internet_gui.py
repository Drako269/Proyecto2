# block_internet_gui.py

import tkinter as tk
from tkinter import messagebox

class BlockInternetFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="¿Estás seguro de bloquear toda la red?").pack(pady=20)

        tk.Button(self, text="Sí, bloquear todo", width=20,
                  command=lambda: messagebox.showinfo("Internet", "Toda la conexión ha sido bloqueada.")).pack(pady=5)

        # Botón que llama a go_back(), donde se hace la importación diferida
        tk.Button(self, text="⬅️ Regresar al Menú", command=self.go_back).pack(pady=5)

    def go_back(self):
        # Importación diferida para evitar ciclo
        from menu_gui import MenuFrame
        self.controller.show_frame(MenuFrame)  # Pasamos la clase, no un string