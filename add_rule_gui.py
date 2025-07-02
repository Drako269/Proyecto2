# add_rule_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from hosts_manager import normalize_domain
from db_manager import (
    create_block_rule,
    rule_exists_for_page,
    get_or_create_blocked_page,
    get_all_blocked_domains
)
from firewall_manager import block_internet


class AddRuleFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg="#B3C1DC")

        # Marco superior para el título
        top_frame = tk.Frame(self, bg="#B3C1DC")
        top_frame.pack(pady=30)

        # Título del formulario
        title_label = tk.Label(
            top_frame,
            text="Agregar Regla De Bloqueo",
            font=("Arial", 18, "bold"),
            bg="#B3C1DC",
            fg="#4C587D"
        )
        title_label.pack()

        separator = ttk.Separator(top_frame, orient="horizontal")
        separator.pack(fill="x", pady=(10, 20))

        # Marco central para formularios
        main_frame = tk.Frame(self, bg="#B3C1DC")
        main_frame.pack(expand=True, fill="both", padx=20)

        # Variable del tipo de bloqueo
        self.rule_type_var = tk.StringVar()
        self.fields_frame = None
        self.check_vars = {}  # Para checkboxes de días

        # Menú desplegable de tipos de bloqueo
        tk.Label(main_frame, text="Tipo de Bloqueo:", bg="#B3C1DC", font=("Arial", 10)).pack(anchor="w")
        self.type_menu = ttk.Combobox(
            main_frame,
            textvariable=self.rule_type_var,
            values=["", "pagina", "internet"],
            state="readonly",
            width=28
        )
        self.type_menu.pack(pady=(0, 15))
        self.type_menu.bind("<<ComboboxSelected>>", self.show_fields)

        # Frame donde se mostrarán los campos dinámicos
        self.dynamic_fields_frame = tk.Frame(main_frame, bg="#B3C1DC")
        self.dynamic_fields_frame.pack(pady=10, fill="x")

        # Botón para crear regla
        self.create_button = tk.Button(
            main_frame,
            text="Crear Regla",
            bg="#788AB2",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.create_rule
        )
        self.create_button.pack(pady=10)
        self.create_button.config(state="disabled")  # Desactivado hasta elegir tipo

        # Botón para regresar
        back_button = tk.Button(
            main_frame,
            text="⬅️ Regresar al Menú",
            bg="#788AB2",
            fg="white",
            font=("Arial", 10),
            relief="flat",
            bd=0,
            command=self.go_back
        )
        back_button.pack(pady=10)

    def go_back(self):
        from menu_gui import MenuFrame
        self.controller.show_frame(MenuFrame)

    def show_fields(self, event=None):
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
        self.fields_frame = tk.Frame(self.dynamic_fields_frame, bg="#B3C1DC")
        self.fields_frame.pack()

        # Campo de fecha - DateEntry (tipo date)
        tk.Label(self.fields_frame, text="Fecha Inicio:", bg="#B3C1DC", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
        self.date_start = DateEntry(
            self.fields_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.date_start.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.fields_frame, text="Fecha Fin:", bg="#B3C1DC", font=("Arial", 10)).grid(row=1, column=0, sticky="w")
        self.date_end = DateEntry(
            self.fields_frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd'
        )
        self.date_end.grid(row=1, column=1, padx=5, pady=5)

        # Campo de Hora Inicio (HH:MM) - Spinboxes
        tk.Label(self.fields_frame, text="Hora Inicio (HH:MM):", bg="#B3C1DC", font=("Arial", 10)).grid(row=2, column=0, sticky="w")

        frame_start_time = tk.Frame(self.fields_frame, bg="#B3C1DC")
        frame_start_time.grid(row=2, column=1, padx=5, pady=5)

        self.hour_start = tk.Spinbox(
            frame_start_time, from_=0, to=23,
            width=2, format="%02.0f", wrap=True
        )
        self.hour_start.pack(side="left")
        tk.Label(frame_start_time, text=":", bg="#B3C1DC").pack(side="left")

        self.minute_start = tk.Spinbox(
            frame_start_time, from_=0, to=59,
            width=2, format="%02.0f", wrap=True
        )
        self.minute_start.pack(side="left")

        # Campo de Hora Fin (HH:MM) - Spinboxes
        tk.Label(self.fields_frame, text="Hora Fin (HH:MM):", bg="#B3C1DC", font=("Arial", 10)).grid(row=3, column=0, sticky="w")

        frame_end_time = tk.Frame(self.fields_frame, bg="#B3C1DC")
        frame_end_time.grid(row=3, column=1, padx=5, pady=5)

        self.hour_end = tk.Spinbox(
            frame_end_time, from_=0, to=23,
            width=2, format="%02.0f", wrap=True
        )
        self.hour_end.pack(side="left")
        tk.Label(frame_end_time, text=":", bg="#B3C1DC").pack(side="left")

        self.minute_end = tk.Spinbox(
            frame_end_time, from_=0, to=59,
            width=2, format="%02.0f", wrap=True
        )
        self.minute_end.pack(side="left")

        # Checkboxes de días de la semana
        tk.Label(self.fields_frame, text="Días de la semana (opcional):", bg="#B3C1DC", font=("Arial", 10)).grid(row=4, column=0, sticky="w")

        days = ["lun", "mar", "mie", "jue", "vie", "sab", "dom"]
        for idx, day in enumerate(days):
            var = tk.BooleanVar()
            self.check_vars[day] = var
            tk.Checkbutton(
                self.fields_frame,
                text=day.upper(),
                variable=var,
                bg="#B3C1DC"
            ).grid(row=4, column=idx + 1, padx=2, pady=5)

        # Campo específico para 'pagina'
        if selected_type == "pagina":
            tk.Label(self.fields_frame, text="Dominio (ej: youtube.com):", bg="#B3C1DC", font=("Arial", 10)).grid(row=5, column=0, sticky="w")

            # Combobox para dominios existentes o nuevo dominio
            self.domain_var = tk.StringVar()
            self.entry_website = ttk.Combobox(
                self.fields_frame,
                textvariable=self.domain_var,
                values=[""] + get_all_blocked_domains(),  # Dominios desde BD
                state="normal",
                width=30
            )
            self.entry_website.grid(row=5, column=1, padx=5, pady=5)
            self.entry_website.current(0)

    def create_rule(self):
        """Crea la regla de bloqueo en base de datos"""
        rule_type = self.rule_type_var.get()
        if not rule_type:
            messagebox.showwarning("Advertencia", "Por favor selecciona un tipo de bloqueo.")
            return

        # Obtener valores comunes
        start_date = self.date_start.get() or None
        end_date = self.date_end.get() or None
        start_time = f"{int(self.hour_start.get()):02d}:{int(self.minute_start.get()):02d}"
        end_time = f"{int(self.hour_end.get()):02d}:{int(self.minute_end.get()):02d}"

        # Validar formato HH:MM
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
            raw_input = self.entry_website.get().strip()
            if not raw_input:
                messagebox.showwarning("Advertencia", "Por favor ingresa un dominio.")
                return

            website = normalize_domain(raw_input)
            if not website:
                messagebox.showerror("Error", "El dominio ingresado no es válido.")
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
            hh, mm = map(int, time_str.split(':'))
            return 0 <= hh < 24 and 0 <= mm < 60
        except Exception:
            return False