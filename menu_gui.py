# menu_gui.py

import tkinter as tk
from tkinter import ttk
from blocked_websites_gui import BlockedWebsitesFrame
from schedule_gui import ScheduleFrame
from history_gui import HistoryFrame
from add_rule_gui import AddRuleFrame
from manual_gui import ManualUsoFrame


class MenuFrame(tk.Frame):
    
    def on_exit(self):
      """Cierra la aplicación"""
      toplevel = self.winfo_toplevel()
      toplevel.destroy()
      
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Configuración del Frame principal
        self.configure(bg="#B3C1DC")
        self.title_frame = tk.Frame(self, bg="#B3C1DC")
        self.title_frame.pack(pady=(100, 50))

        # Título del aplicativo
        tk.Label(
            self.title_frame,
            text="SafeWeb",
            font=("Arial", 24, "bold"),
            bg="#B3C1DC",
            fg="#4C587D"
        ).pack()

        # Línea divisoria opcional (solo para estilo visual)
        separator = ttk.Separator(self.title_frame, orient="horizontal")
        separator.pack(fill="x", pady=(10, 0))

        # Marco para botones - centrado
        buttons_frame = tk.Frame(self, bg="#B3C1DC")
        buttons_frame.pack(expand=True)

        # Función auxiliar para crear botones con estilo
        def create_styled_button(parent, text, frame_class):
            btn = tk.Button(
                parent,
                text=text,
                width=30,
                bg="#788AB2",
                fg="white",
                font=("Arial", 12, "bold"),
                relief="flat",
                padx=10,
                pady=6,
                command=lambda: controller.show_frame(frame_class) if frame_class != "exit" else controller.quit()
            )
            btn.pack(pady=10)

        # Botones del menú
        create_styled_button(buttons_frame, "➕ Agregar Regla de Bloqueo", AddRuleFrame)
        create_styled_button(buttons_frame, "🔒 Páginas Bloqueadas", BlockedWebsitesFrame)
        create_styled_button(buttons_frame, "📅 Cronograma de Uso", ScheduleFrame)
        create_styled_button(buttons_frame, "📜 Historial de Búsquedas", HistoryFrame)
        create_styled_button(buttons_frame, "Manual de Uso", ManualUsoFrame)

        # Botón salir
        exit_btn = tk.Button(
            buttons_frame,
            text="🚪 Salir",
            width=30,
            bg="#E63946",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            padx=10,
            pady=6,
            command=self.on_exit
        )
        exit_btn.pack(pady=10)

        # Centrar ventana al mostrar
        self.center_window()
    
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.update_idletasks()
        width = 900
        height = 700

        toplevel = self.winfo_toplevel()
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Aplicar estilo al toplevel
        toplevel.configure(
            bg="#B3C1DC",
            highlightbackground="#4C587D",  # Borde de ventana
            highlightthickness=20
        )
        toplevel.geometry(f"{width}x{height}+{x}+{y}")

        