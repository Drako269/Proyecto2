# schedule_gui.py

import tkinter as tk

class ScheduleFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Configura el tiempo de acceso a internet", font=("Arial", 12)).pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Hora inicio:").grid(row=0, column=0)
        start_hour = tk.Entry(frame, width=5)
        start_hour.grid(row=0, column=1)

        tk.Label(frame, text="Hora fin:").grid(row=0, column=2)
        end_hour = tk.Entry(frame, width=5)
        end_hour.grid(row=0, column=3)

        tk.Button(self, text="Guardar horario", width=20).pack(pady=10)

        # ✅ Ahora usamos go_back() en lugar de lambda con cadena
        tk.Button(self, text="⬅️ Regresar al Menú", width=20,
                  command=self.go_back).pack(pady=5)

    def go_back(self):
        # Importación diferida para evitar ciclo
        from menu_gui import MenuFrame
        self.controller.show_frame(MenuFrame)  # Pasamos la clase, no un string