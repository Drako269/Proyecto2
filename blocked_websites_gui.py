# blocked_websites_gui.py

import tkinter as tk
from tkinter import ttk, messagebox, BooleanVar
from db_manager import get_all_block_rules, toggle_rule_active_status
from background_service import start_background_service
from functools import partial


class BlockedWebsitesFrame(tk.Frame):
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
            text="Páginas Bloqueadas",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#788AB2"
        )
        title_label.pack(pady=(0, 15))

        # Marco para listado de reglas
        self.rules_frame = tk.Frame(inner_frame, bg="white")
        self.rules_frame.pack(fill="both", expand=True)

        # Scrollbar opcional (si hay muchas reglas)
        canvas = tk.Canvas(self.rules_frame, bg="white")
        scrollbar = ttk.Scrollbar(self.rules_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.scrollable_frame = scrollable_frame

        # Botones inferiores
        button_frame = tk.Frame(inner_frame, bg="white")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="🔄 Recargar",
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

    def load_data(self):
        """Carga todas las reglas de bloqueo y las muestra como bloques con botones"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        rules = get_all_block_rules()
        if not rules:
            tk.Label(self.scrollable_frame, text="No hay reglas creadas aún.", bg="white", fg="#333").pack(pady=10)
            return

        for idx, rule in enumerate(rules):
            dominio = rule[1]
            tipo_bloqueo = rule[2]
            start_date = rule[3]
            end_date = rule[4]
            dias_semana = rule[5]
            hora_inicio = rule[6]
            hora_fin = rule[7]
            activo = rule[8]  # Este valor ya es booleano (True/False)
            id_regla = rule[9]

            # Marco individual para cada regla
            rule_frame = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid", padx=100, pady=10)
            rule_frame.pack(fill="x", padx=100, pady=5, expand=True)

            # Marco para toda la información de la regla
            info_frame = tk.Frame(rule_frame, bg="white")
            info_frame.pack(side="left", fill="both", expand=True)

            # Mostrar toda la información en líneas separadas
            tk.Label(info_frame, text=f"🌐 Dominio: {dominio}", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
            tk.Label(info_frame, text=f"Tipo: {tipo_bloqueo}", bg="white", font=("Arial", 9)).pack(anchor="w", pady=2)

            # Usar función para formatear
            formatted_start = format_date(start_date)
            formatted_end = format_date(end_date)

            tk.Label(info_frame, text=f"📅 Fechas: {formatted_start} - {formatted_end}",
                    bg="white", font=("Arial", 9)).pack(anchor="w", pady=2)

            if hora_inicio or hora_fin:
                tk.Label(info_frame, text=f"⏰ Horario: {hora_inicio or 'N/A'} - {hora_fin or 'N/A'}",
                        bg="white", font=("Arial", 9)).pack(anchor="w", pady=2)

            if dias_semana:
                tk.Label(info_frame, text=f"🗓 Días: {dias_semana}", bg="white", font=("Arial", 9)).pack(anchor="w", pady=2)

            # Botones de acción - derecha
            actions_frame = tk.Frame(rule_frame, bg="white")
            actions_frame.pack(side="right")

            # Botón: Activar/Desactivar
            def make_toggle_command(rid=id_regla, status=activo):
                return lambda: self.toggle_rule(rid, not status)

            toggle_text = "Desactivar" if activo else "Activar"
            toggle_color = "#E63946" if activo else "#788AB2"

            toggle_btn = tk.Button(
                actions_frame,
                text=toggle_text,
                bg=toggle_color,
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                width=10,
                command=make_toggle_command(id_regla, activo)
            )
            toggle_btn.pack(pady=2)


            # Botón: Eliminar
            def make_delete_command(rid=id_regla):
                return lambda: self.delete_rule(rid)

            delete_btn = tk.Button(
                actions_frame,
                text="Eliminar",
                bg="#D62828",
                fg="white",
                font=("Arial", 10, "bold"),
                relief="flat",
                width=10,
                command=make_delete_command(id_regla)
            )
            delete_btn.pack(pady=2)

  


    def toggle_rule(self, rule_id, new_status):
        success = toggle_rule_active_status(rule_id, new_status)
        if success:
            messagebox.showinfo("Éxito", f"Regla {rule_id} {'desactivada' if new_status else 'activada'}")
            self.load_data()
        else:
            messagebox.showerror("Error", f"No se pudo actualizar la regla {rule_id}")

    def go_back(self):
        from menu_gui import MenuFrame
        self.controller.show_frame(MenuFrame)


    def delete_rule(self, rule_id):
        """Pregunta confirmación y elimina la regla"""
        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar esta regla?")
        if not confirm:
            return

        from db_manager import delete_block_rule
        success = delete_block_rule(rule_id)
        if success:
            messagebox.showinfo("Éxito", f"Regla eliminada correctamente.")
            self.load_data()  # Recargar lista
        else:
            messagebox.showerror("Error", "No se pudo eliminar la regla.")


def create_action_button(parent, text, command):
    """Helper para crear botones dentro de Treeview"""
    btn = tk.Button(parent, text=text, command=command)
    return btn

def format_date(date_obj):
    """Convierte una fecha de YYYY-MM-DD a DD/MM/YYYY"""
    if not date_obj:
        return "N/A"
    try:
        # Si es string (ej: '2025-04-05')
        if isinstance(date_obj, str):
            y, m, d = date_obj.split('-')
        # Si es objeto datetime.date
        else:
            y, m, d = str(date_obj.year), str(date_obj.month).zfill(2), str(date_obj.day).zfill(2)
        return f"{d}/{m}/{y}"
    except:
        return "N/A"  