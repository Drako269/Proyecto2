# blocked_websites_gui.py

import tkinter as tk
from tkinter import ttk, messagebox, BooleanVar
from db_manager import get_all_block_rules, toggle_rule_active_status
from background_service import start_background_service


class BlockedWebsitesFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Páginas Bloqueadas", font=("Arial", 16)).pack(pady=15)

        # Frame contenedor de tabla + scroll
        frame_table = tk.Frame(self)
        frame_table.pack(fill="both", expand=True, padx=10)

        # Tabla de reglas
        self.tree = ttk.Treeview(frame_table, columns=(
            "Dominio", "Tipo Bloqueo", "Fecha Inicio", "Fecha Fin",
            "Días Semana", "Hora Inicio", "Hora Fin", "Activo"
        ), show="headings", height=15)

        # Configurar columnas
        cols = [
            ("Dominio", 120),
            ("Tipo Bloqueo", 100),
            ("Fecha Inicio", 100),
            ("Fecha Fin", 100),
            ("Días Semana", 100),
            ("Hora Inicio", 80),
            ("Hora Fin", 80),
            ("Activo", 120),
        ]

        for col, width in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor=tk.CENTER if col == "Activo" else tk.W)

        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Frame para los botones - posicionado sobre la columna "Activo"
        self.btn_frame = tk.Frame(self.tree)
        self.btn_frame.place(relx=0.93, rely=0, relheight=1, relwidth=0.17)  # Ajuste visual

        self.buttons = {}  # Diccionario para mantener referencias a los botones

        # Cargar datos
        self.load_data()

        # Botones inferiores
        tk.Button(self, text="🔄 Recargar", command=self.load_data).pack(pady=5)
        tk.Button(self, text="⬅️ Regresar al Menú", command=self.go_back).pack(pady=10)

    def load_data(self):
        """Carga todas las reglas de bloqueo y agrega Checkbutton en 'Activo'"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        rules = get_all_block_rules()
        self.buttons.clear()

        for idx, rule in enumerate(rules):
            dominio = rule[1]
            tipo_bloqueo = rule[2]
            fecha_inicio = rule[3]
            fecha_fin = rule[4]
            dias_semana = rule[5]
            hora_inicio = rule[6]
            hora_fin = rule[7]
            activo = rule[8]  # Este valor ya es booleano (True/False)
            id_regla = rule[9]

            values = (
                dominio,
                tipo_bloqueo,
                fecha_inicio or "",
                fecha_fin or "",
                dias_semana or "",
                hora_inicio or "",
                hora_fin or "",
                "",  # Esta celda será ocupada por el Checkbutton
            )

            item_id = self.tree.insert("", tk.END, values=values)

            # Crear variable Tkinter para el Checkbutton
            var = tk.BooleanVar(value=activo)

            # Definimos el comando del Checkbutton
            def make_command(rid=id_regla, var=var):
                return lambda: self.toggle_rule(rid, var.get())

            # Creamos el Checkbutton y lo colocamos alineado con la fila
            cb = tk.Checkbutton(
                self.btn_frame,
                variable=var,
                onvalue=True,
                offvalue=False,
                command=make_command(),
                bg="white",
                width=20,
                anchor="w"
            )
            cb.grid(row=idx, column=0, padx=2, pady=2)
            self.buttons[item_id] = cb  # Guardamos referencia
    

    def toggle_rule(self, rule_id, new_status):
        success = toggle_rule_active_status(rule_id, new_status)
        if success:
            messagebox.showinfo("Éxito", f"Regla {rule_id} {'activada' if new_status else 'desactivada'}")
            
            # Llama al servicio de fondo para actualizar hosts
            start_background_service()
        else:
            messagebox.showerror("Error", f"No se pudo actualizar la regla {rule_id}")

    def go_back(self):
        from menu_gui import MenuFrame
        self.controller.show_frame(MenuFrame)

    def toggle_active_status(self, item):
        """Activa o desactiva una regla de bloqueo"""
        values = self.tree.item(item)['values']
        if not values:
            return

        id_regla = values[-1]  # Última columna es el ID de la regla
        current_status = values[7] == "Sí"  # "Activo" está en posición 7

        new_status = not current_status
        success = toggle_rule_active_status(id_regla, new_status)

        if success:
            self.load_data()  # Recargar datos
            messagebox.showinfo("Éxito", f"Regla {id_regla} {'activada' if new_status else 'desactivada'}")
        else:
            messagebox.showerror("Error", "No se pudo actualizar el estado de la regla.")


def create_action_button(parent, text, command):
    """Helper para crear botones dentro de Treeview"""
    btn = tk.Button(parent, text=text, command=command)
    return btn