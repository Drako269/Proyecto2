# add_rule_edit_gui.py

# add_rule_edit_gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from hosts_manager import normalize_domain
from db_manager import get_or_create_blocked_page, update_block_rule


class AddRuleFrameEdit(tk.Frame):
    @staticmethod
    def _time_to_str(t):
        if t is None:
         return f"{t.hour:02d}:{t.minute:02d}"

    def __init__(self, parent, controller, is_editing=False, rule_id=None, rule_data=None):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.is_editing = is_editing
        self.rule_id = rule_id
        self.configure(bg="#B3C1DC")

        # Extraer datos de rule_data
        dominio = rule_data[1]
        tipo_bloqueo = rule_data[2]
        start_date = rule_data[3]
        end_date = rule_data[4]
        dias_semana_str = rule_data[5]  # lun,mar,vie

        hora_inicio_obj = rule_data[6]  # datetime.time
        hora_fin_obj = rule_data[7]

        activo = rule_data[8]
        id_regla = rule_data[9]

        # Función para convertir datetime.time a "HH:MM"


        hora_inicio = AddRuleFrameEdit._time_to_str(hora_inicio_obj)
        hora_fin = AddRuleFrameEdit._time_to_str(hora_fin_obj)

        # Marco superior
        top_frame = tk.Frame(self, bg="#B3C1DC")
        top_frame.pack(pady=30)

        title_label = tk.Label(
            top_frame,
            text="Editar Regla De Bloqueo",
            font=("Arial", 18, "bold"),
            bg="#B3C1DC",
            fg="#4C587D"
        )
        title_label.pack()

        separator = ttk.Separator(top_frame, orient="horizontal")
        separator.pack(fill="x", pady=(10, 20))

        main_frame = tk.Frame(self, bg="#B3C1DC")
        main_frame.pack(expand=True, fill="both", padx=20)

        # Variables
        self.rule_type_var = tk.StringVar(value=tipo_bloqueo)
        self.fields_frame = None
        self.check_vars = {}

        # Tipo de bloqueo
        tk.Label(main_frame, text="Tipo de Bloqueo:", bg="#B3C1DC", font=("Arial", 10)).pack(anchor="w")
        self.type_menu = ttk.Combobox(
            main_frame,
            textvariable=self.rule_type_var,
            values=["pagina", "internet"],
            state="readonly",
            width=28
        )
        self.type_menu.pack(pady=(0, 15))
        self.type_menu.bind("<<ComboboxSelected>>", self.show_fields)

        # Frame dinámico
        self.dynamic_fields_frame = tk.Frame(main_frame, bg="#B3C1DC")
        self.dynamic_fields_frame.pack(pady=10, fill="x")

        # Botón guardar
        save_btn = tk.Button(
            main_frame,
            text="Guardar Cambios",
            bg="#788AB2",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=lambda: self.save_changes(dominio)
        )
        save_btn.pack(pady=10)

        back_btn = tk.Button(
            main_frame,
            text="⬅️ Cancelar",
            bg="#E63946",
            fg="white",
            font=("Arial", 10),
            relief="flat",
            command=self.go_back
        )
        back_btn.pack(pady=10)

        # Mostrar campos
        self.show_fields()

        # Poblar campos existentes
        if start_date:
            self.date_start.set_date(start_date)
        if end_date:
            self.date_end.set_date(end_date)

        if hora_inicio and ':' in hora_inicio:
            h, m = hora_inicio.split(':')
            self.hour_start.delete(0, 'end')
            self.hour_start.insert(0, h)
            self.minute_start.delete(0, 'end')
            self.minute_start.insert(0, m)

        if hora_fin and ':' in hora_fin:
            h, m = hora_fin.split(':')
            self.hour_end.delete(0, 'end')
            self.hour_end.insert(0, h)
            self.minute_end.delete(0, 'end')
            self.minute_end.insert(0, m)

        # Días de la semana
        if dias_semana_str:
            dias_list = [d.strip() for d in dias_semana_str.split(',')]
            for day, var in self.check_vars.items():
                if day in dias_list:
                    var.set(True)

        # Dominio
        if tipo_bloqueo == "pagina":
            if dominio:  # Solo si hay dominio
                self.domain_var.set(dominio)  # ✅ Correcto: usa la variable, no el widget

    def go_back(self):
        from blocked_websites_gui import BlockedWebsitesFrame
        self.controller.show_frame(BlockedWebsitesFrame)

    def show_fields(self, event=None):
        selected_type = self.rule_type_var.get()
        if self.fields_frame:
            self.fields_frame.destroy()
            self.check_vars.clear()

        self.fields_frame = tk.Frame(self.dynamic_fields_frame, bg="#B3C1DC")
        self.fields_frame.pack()

        # Fecha Inicio
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

        # Fecha Fin
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

        # Hora Inicio
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

        # Hora Fin
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

        # Días de la semana
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
            self.domain_var = tk.StringVar()
            self.entry_website = ttk.Entry(
                self.fields_frame,
                textvariable=self.domain_var,
                width=30
            )
            self.entry_website.grid(row=5, column=1, padx=5, pady=5)

    def save_changes(self, current_dominio):
        """Guarda los cambios actualizando la regla"""
        rule_type = self.rule_type_var.get()
        if not rule_type:
            messagebox.showwarning("Advertencia", "Por favor selecciona un tipo de bloqueo.")
            return

        # Obtener valores
        start_date = self.date_start.get_date().strftime("%Y-%m-%d") if self.date_start.get_date() else None
        end_date = self.date_end.get_date().strftime("%Y-%m-%d") if self.date_end.get_date() else None

        try:
            start_hour = int(self.hour_start.get())
            start_minute = int(self.minute_start.get())
            hora_inicio = f"{start_hour:02d}:{start_minute:02d}"
        except:
            hora_inicio = None

        try:
            end_hour = int(self.hour_end.get())
            end_minute = int(self.minute_end.get())
            hora_fin = f"{end_hour:02d}:{end_minute:02d}"
        except:
            hora_fin = None

        # Limpiar horas iguales
        if hora_inicio and hora_fin and hora_inicio == hora_fin:
            hora_inicio = None
            hora_fin = None

        # Días seleccionados
        days_selected = [day for day, var in self.check_vars.items() if var.get()]
        dias_semana = ",".join(days_selected) if days_selected else None

        # Procesar dominio
        website = current_dominio
        if rule_type == "pagina":
            raw_input = self.entry_website.get().strip()
            if raw_input:
                website = normalize_domain(raw_input)
                if not website:
                    messagebox.showerror("Error", "El dominio ingresado no es válido.")
                    return

        page_id = get_or_create_blocked_page(website)
        if not page_id:
            messagebox.showerror("Error", f"No se pudo registrar {website} en la base de datos.")
            return

        # Actualizar regla
        success = update_block_rule(
            rule_id=self.rule_id,
            page_id=page_id,
            rule_type=rule_type,
            fecha_inicio=start_date,
            fecha_fin=end_date,
            dias_semana=dias_semana,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin
        )

        if success:
            messagebox.showinfo("Éxito", "Regla actualizada correctamente.")
            from blocked_websites_gui import BlockedWebsitesFrame
            self.controller.show_frame(BlockedWebsitesFrame)
        else:
            messagebox.showerror("Error", "No se pudo actualizar la regla.")