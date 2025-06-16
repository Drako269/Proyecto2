# menu_gui.py

import tkinter as tk
from block_website_gui import BlockWebsiteFrame
from blocked_websites_gui import BlockedWebsitesFrame
from block_internet_gui import BlockInternetFrame
from schedule_gui import ScheduleFrame
from history_gui import HistoryFrame
from add_rule_gui import AddRuleFrame

class MenuFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Seleccione una opción", font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="➕ Agregar Regla de Bloqueo", width=30,
                  command=lambda: controller.show_frame(AddRuleFrame)).pack(pady=10)
        tk.Button(self, text="🚫 Bloquear Página", width=30,
                  command=lambda: controller.show_frame(BlockWebsiteFrame)).pack(pady=10)
        tk.Button(self, text="🔒 Páginas Bloqueadas", width=30,
                  command=lambda: controller.show_frame(BlockedWebsitesFrame)).pack(pady=10)
        tk.Button(self, text="🌐 Bloquear Internet", width=30,
                  command=lambda: controller.show_frame(BlockInternetFrame)).pack(pady=10)
        tk.Button(self, text="📅 Cronograma de Uso", width=30,
                  command=lambda: controller.show_frame(ScheduleFrame)).pack(pady=10)
        tk.Button(self, text="📜 Historial de Búsquedas", width=30,
          command=lambda: controller.show_frame(HistoryFrame)).pack(pady=10)

        tk.Button(self, text="Salir", width=30, command=self.quit).pack(pady=15)

        