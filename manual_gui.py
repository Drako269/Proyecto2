# manual_gui.py

import tkinter as tk
from tkinter import ttk


class ManualUsoFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Configuración del fondo y estilo
        self.configure(bg="#B3C1DC")
        outer_frame = tk.Frame(self, bg="#B3C1DC", highlightbackground="#4C587D", highlightthickness=2)
        outer_frame.pack(padx=10, pady=10, expand=True, fill="both")

        inner_frame = tk.Frame(outer_frame, bg="white")
        inner_frame.pack(padx=20, pady=20, expand=True, fill="both")

        # Título
        title_label = tk.Label(
            inner_frame,
            text="Manual de Uso - Control Parental",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="#788AB2"
        )
        title_label.pack(pady=(0, 15))

        # Marco con Canvas para desplazamiento
        scroll_frame = tk.Frame(inner_frame)
        scroll_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(scroll_frame, bg="white")
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Contenido del manual
        manual_text = """\n\n
1. 🔐 Inicio de Sesión
   - Abre la aplicación.
   - Ingresa tu usuario y contraseña.
   - Haz clic en 'Iniciar Sesión'.
   - Si las credenciales son incorrectas, se muestra un mensaje de error.

2. 🧭 Menú Principal
   - Una vez autenticado, accedes al menú principal.
   - Opciones disponibles:
     • ➕ Agregar Regla de Bloqueo
     • 🚫 Bloquear Página
     • 🔒 Páginas Bloqueadas
     • 📜 Historial de Búsquedas
     • 📚 Manual de Uso (estás aquí)

3. ✅ Agregar Regla de Bloqueo
   - Selecciona el tipo de bloqueo:
     • página → bloquea un dominio específico
     • internet → bloquea todo el tráfico saliente
   - Define:
     • Fecha Inicio / Fecha Fin
     • Hora Inicio / Hora Fin
     • Días de la semana (opcional)
     • Dominio (solo si es tipo "pagina")
   - Haz clic en 'Crear Regla' para guardarla en la BD y actualizar hosts.

4. 🛑 Páginas Bloqueadas
   - Muestra todas las páginas actualmente bloqueadas.
   - Cada regla tiene un Checkbutton que permite activar/desactivar el bloqueo.
   - Botones:
     • 🔄 Recargar → actualiza la lista desde la BD
     • ⬅️ Regresar al Menú → vuelve al menú principal

5. 📜 Historial de Búsquedas
   - Muestra automáticamente las páginas visitadas por el usuario.
   - Datos mostrados:
     • URL Visitada
     • Dominio
     • Fecha
     • Hora
   - Botones:
     • 🔄 Recargar → actualiza los datos desde la BD
     • ⬅️ Regresar al Menú → vuelve al menú principal

6. ⚙ Notas técnicas
   - Las reglas se guardan en PostgreSQL (`reglas_bloqueo`)
   - El archivo hosts se actualiza automáticamente al crear/editar una regla
   - El historial se guarda en la tabla `registros_visitas`
   - Funciona mejor ejecutando como administrador (para modificar el archivo hosts)
        """

        manual_label = tk.Label(
            scrollable_frame,
            text=manual_text,
            justify="left",
            wraplength=350,
            font=("Arial", 12),
            bg="white",
            fg="#333"
        )
        manual_label.pack(anchor="w", padx=10, pady=5)

        # Botón fijo en la parte inferior de la ventana (fuera del scroll)
        button_frame = tk.Frame(self, bg="#B3C1DC")
        button_frame.pack(pady=10, fill="x", side="bottom")

        back_button = tk.Button(
            button_frame,
            text="⬅️ Regresar al Menú",
            bg="#788AB2",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            command=self.go_back
        )
        back_button.pack()

    def go_back(self):
        from menu_gui import MenuFrame
        self.controller.show_frame(MenuFrame)