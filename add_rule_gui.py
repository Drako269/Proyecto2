# add_rule_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db_manager import create_block_rule, rule_exists_for_page, get_or_create_blocked_page


class AddRuleFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Título
        tk.Label(self, text="Agregar Regla De Bloqueo", font=("Arial", 16)).pack(pady=15)

        # Variable del tipo de bloqueo
        self.rule_type_var = tk.StringVar()
        self.fields_frame = None
        self.check_vars = {}  # Para checkboxes de días

        # Menú desplegable de tipos de bloqueo
        tk.Label(self, text="Tipo de Bloqueo:").pack(pady=5)
        self.type_menu = ttk.Combobox(
            self,
            textvariable=self.rule_type_var,
            values=["", "pagina", "internet"],
            state="readonly",
            width=28
        )
        self.type_menu.pack(pady=5)
        self.type_menu.bind("<<ComboboxSelected>>", self.show_fields)

        # Frame donde se mostrarán los campos según tipo de bloqueo
        self.dynamic_fields_frame = tk.Frame(self)
        self.dynamic_fields_frame.pack(pady=10, fill="x")

        # Botón para crear la regla
        self.create_button = tk.Button(self, text="Crear Regla", command=self.create_rule)
        self.create_button.pack(pady=10)
        self.create_button.config(state="disabled")  # Desactivado hasta elegir tipo

        # Botón para regresar al menú
        tk.Button(self, text="⬅️ Regresar al Menú", command=self.go_back).pack(pady=10)

    def go_back(self):
        from menu_gui import MenuFrame
        self.controller.show_frame(MenuFrame)

    def show_fields(self, event=None):
        """Muestra campos según el tipo de bloqueo seleccionado"""
        selected_type = self.rule_type_var.get()

        if self.fields_frame:
            self.fields_frame.destroy()
            self.check_vars.clear()

        if selected_type == "":
            self.create_button.config(state="disabled")
            return
        else:
            self.create_button.config(state="normal")

        # Mostrar campos dinámicos
        self.fields_frame = tk.Frame(self.dynamic_fields_frame)
        self.fields_frame.pack()

        # Campo de fecha - DateEntry (tipo date)
        tk.Label(self.fields_frame, text="Fecha Inicio:").grid(row=0, column=0, sticky="w")
        self.date_start = DateEntry(self.fields_frame, width=12, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_start.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.fields_frame, text="Fecha Fin:").grid(row=1, column=0, sticky="w")
        self.date_end = DateEntry(self.fields_frame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_end.grid(row=1, column=1, padx=5, pady=5)

        # Campos de hora - Inputs de texto con validación numérica
        tk.Label(self.fields_frame, text="Hora Inicio (HH:MM):").grid(row=2, column=0, sticky="w")
        self.entry_start_time = tk.Entry(self.fields_frame)
        self.entry_start_time.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.fields_frame, text="Hora Fin (HH:MM):").grid(row=3, column=0, sticky="w")
        self.entry_end_time = tk.Entry(self.fields_frame)
        self.entry_end_time.grid(row=3, column=1, padx=5, pady=5)

        # Checkboxes de días de la semana
        days = ["lun", "mar", "mie", "jue", "vie", "sab", "dom"]
        tk.Label(self.fields_frame, text="Días de la semana (opcional):").grid(row=4, column=0, sticky="w")

        for idx, day in enumerate(days):
            var = tk.BooleanVar()
            self.check_vars[day] = var
            tk.Checkbutton(self.fields_frame, text=day.upper(), variable=var).grid(
                row=4, column=idx + 1, padx=2, pady=5
            )

        # Campo específico para 'pagina'
        if selected_type == "pagina":
            tk.Label(self.fields_frame, text="Dominio (ej: youtube.com):").grid(row=5, column=0, sticky="w")
            self.entry_website = tk.Entry(self.fields_frame, width=30)
            self.entry_website.grid(row=5, column=1, padx=5, pady=5)

    def create_rule(self):
        """Crea la regla de bloqueo en base de datos"""
        rule_type = self.rule_type_var.get()
        if not rule_type:
            messagebox.showwarning("Advertencia", "Por favor selecciona un tipo de bloqueo.")
            return

        # Obtener valores comunes
        start_date = self.date_start.get() or None
        end_date = self.date_end.get() or None
        start_time = self.entry_start_time.get().strip() or None
        end_time = self.entry_end_time.get().strip() or None

        # Validar formato de hora HH:MM
        if start_time and not self._is_valid_time(start_time):
            messagebox.showerror("Error", "Formato inválido en Hora Inicio. Usa HH:MM")
            return

        if end_time and not self._is_valid_time(end_time):
            messagebox.showerror("Error", "Formato inválido en Hora Fin. Usa HH:MM")
            return

        # Días seleccionados
        days_selected = [day for day, var in self.check_vars.items() if var.get()]
        days_str = ",".join(days_selected) if days_selected else None

        if rule_type == "pagina":
            website = self.entry_website.get().strip()
            if not website:
                messagebox.showwarning("Advertencia", "Por favor ingresa un dominio.")
                return

            page_id = get_or_create_blocked_page(website)
            if not page_id:
                messagebox.showerror("Error", f"No se pudo registrar {website} en la base de datos.")
                return

            if rule_exists_for_page(page_id):
                messagebox.showwarning("Advertencia", "Esta regla ya fue creada anteriormente.")
                return

            success = create_block_rule(
                page_id=page_id,
                rule_type=rule_type,
                fecha_inicio=start_date,
                fecha_fin=end_date,
                dias_semana=days_str,
                hora_inicio=start_time,
                hora_fin=end_time
            )

            if success:
                messagebox.showinfo("Éxito", f"Regla creada para '{website}'")
            else:
                messagebox.showerror("Error", "No se pudo crear la regla.")

        elif rule_type == "internet":
            # Usamos un dominio especial para representar internet completo
            page_id = get_or_create_blocked_page("internet_global")
            if not page_id:
                messagebox.showerror("Error", "No se pudo crear la regla para Internet.")
                return

            if rule_exists_for_page(page_id):
                messagebox.showwarning("Advertencia", "Ya existe una regla idéntica para Internet.")
                return

            success = create_block_rule(
                page_id=page_id,
                rule_type=rule_type,
                fecha_inicio=start_date,
                fecha_fin=end_date,
                dias_semana=days_str,
                hora_inicio=start_time,
                hora_fin=end_time
            )

            if success:
                messagebox.showinfo("Éxito", "Regla creada para Bloquear Internet")
            else:
                messagebox.showerror("Error", "No se pudo crear la regla.")

    def _is_valid_time(self, time_str):
        """Valida que el tiempo esté en formato HH:MM"""
        try:
            hh, mm = map(int, time_str.split(":"))
            return 0 <= hh < 24 and 0 <= mm < 60
        except Exception:
            return False