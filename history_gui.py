# history_gui.py

import tkinter as tk
from tkinter import ttk
from db_manager import get_website_history  # Función que vamos a crear ahora

class HistoryFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Historial de Búsquedas", font=("Arial", 14)).pack(pady=10)

        # Tabla para mostrar historial
        cols = ("URL Visitada", "Dominio", "Fecha", "Bloqueada", "Razón")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=10)

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Botón para recargar datos
        tk.Button(self, text="🔄 Recargar Historial", command=self.load_data).pack(pady=5)

        # Botón para regresar
        tk.Button(self, text="⬅️ Regresar al Menú", command=self.go_back).pack(pady=5)

        # Cargar datos al iniciar
        self.load_data()

    def load_data(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener historial
        history = get_website_history()
        for record in history:
            self.tree.insert("", tk.END, values=record)

    def go_back(self):
        from menu_gui import MenuFrame
        self.controller.show_frame(MenuFrame)