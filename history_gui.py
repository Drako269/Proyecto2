# history_gui.py

import tkinter as tk
from tkinter import ttk
from db_manager import get_website_history
from datetime import datetime
import webbrowser


class HistoryFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Configuración visual
        self.configure(bg="#B3C1DC")
        outer_frame = tk.Frame(self, bg="#B3C1DC", highlightbackground="#4C587D",
                               highlightthickness=2, bd=0)
        outer_frame.pack(padx=20, pady=20, expand=True, fill="both")

        inner_frame = tk.Frame(outer_frame, bg="white")
        inner_frame.pack(padx=20, pady=20, expand=True, fill="both")

        # Título
        title_label = tk.Label(
            inner_frame,
            text="Historial de Búsquedas",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#788AB2"
        )
        title_label.pack(pady=(0, 15))

        # Tabla de historial
        cols = ("URL Visitada", "Dominio", "Fecha", "Hora")
        self.tree = ttk.Treeview(inner_frame, columns=cols, show="headings", height=15)

        column_widths = {
            "URL Visitada": 250,
            "Dominio": 150,
            "Fecha": 100,
            "Hora": 80
        }

        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col], anchor="w")

        self.tree.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(inner_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Evento de doble clic → abrir URL
        self.tree.bind("<Double-1>", self.open_url_from_tree)  # ✅ Nuevo evento

        # Botones inferiores
        button_frame = tk.Frame(inner_frame, bg="white")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="🔄 Recargar Historial",
            bg="#788AB2",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.load_data
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="⬅️ Regresar al Menú",
            bg="#788AB2",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.go_back
        ).pack(side="left", padx=10)

        # Cargar datos al iniciar
        self.load_data()

    def go_back(self):
        from menu_gui import MenuFrame
        self.controller.show_frame(MenuFrame)

    def load_data(self):
        """Carga historial desde BD y muestra Fecha y Hora por separado"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        history = get_website_history(limit=100)
        for record in history:
            url_visitada, dominio, fecha_hora = record

            # Si fecha_hora es un objeto datetime
            if isinstance(fecha_hora, datetime):
                fecha = fecha_hora.strftime("%Y-%m-%d")
                hora = fecha_hora.strftime("%H:%M")
            else:
                try:
                    # Si es string, dividimos
                    if fecha_hora and " " in fecha_hora:
                        fecha_part, hora_part = fecha_hora.split(" ", 1)
                        fecha = fecha_part
                        hora = hora_part[:5]  # Tomar solo HH:MM
                    else:
                        fecha = ""
                        hora = ""
                except Exception as e:
                    print(f"⚠️ Error al procesar fecha/hora: {e}")
                    fecha = ""
                    hora = ""

            self.tree.insert("", tk.END, values=(url_visitada, dominio, fecha, hora))

    def open_url_from_tree(self, event):
        """Abre la URL visitada en el navegador"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        values = self.tree.item(selected_item, "values")
        if values:
            url = values[0]
            print(f"🌐 Abriendo URL: {url}")
            webbrowser.open(url)
        
