# auth_gui.py

import tkinter as tk
from tkinter import messagebox, Frame, ttk
import db_manager
from PIL import Image, ImageTk


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SafeWeb - Inicio de Sesión")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        # Cargar la imagen de fondo
        bg_image = Image.open("imagen/familia.jpg")  # Reemplaza "background.png" con la ruta de tu imagen
        bg_image = bg_image.resize((500, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Crear Canvas para la imagen de fondo
        self.canvas = tk.Canvas(self.root, width=400, height=600, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)

        # Colocar imagen de fondo en el canvas
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Campo de usuario con placeholder
        self.entry_user = tk.Entry(
            self.root,
            font=("Arial", 12),
            bd=0,
            relief="flat",
            bg="#ffffff",
            fg="#000000",
            justify="center"
        )

        # Insertar texto inicial
        self.entry_user.insert(0, "Usuario")
        self.entry_user.bind("<FocusIn>", self.on_entry_click)
        self.entry_user.bind("<FocusOut>", self.on_focus_out)

        # Guardamos el valor original como atributo del widget
        self.entry_user.default_text = "Usuario"

        self.canvas.create_window(200, 360, window=self.entry_user, width=250)

        # Campo de contraseña con placeholder
        self.entry_pass = tk.Entry(
            self.root,
            font=("Arial", 12),
            bd=0,
            relief="flat",
            bg="#ffffff",
            fg="#000000",
            justify="center"
        )

        self.entry_pass.insert(0, "Contraseña")
        self.entry_pass.bind("<FocusIn>", self.on_entry_click)
        self.entry_pass.bind("<FocusOut>", self.on_focus_out)
        self.entry_pass.default_text = "Contraseña"
        self.entry_pass.config(show="")  # Mostrar texto normal hasta que se escriba

        self.canvas.create_window(200, 430, window=self.entry_pass, width=250)

        # Título del aplicativo
        title_text = "SafeWeb"

        # Medidas del rectángulo redondeado (ajustables)
        rect_x = 120  # Posición X inicial
        rect_y = 75   # Posición Y inicial
        rect_width = 160  # Ancho del rectángulo
        rect_height = 50  # Alto del rectángulo
        radius = 15       # Radio de las esquinas

        # Dibujar el rectángulo redondeado como fondo del título
        self.rounded_rectangle(
            self.canvas,
            rect_x, rect_y,
            rect_x + rect_width,
            rect_y + rect_height,
            radius=radius,
            fill="#ffffff",     # Color de fondo
            outline="#dddddd",  # Borde (opcional)
            width=1             # Grosor del borde
        )

        # Crear el Label encima del rectángulo
        title_label = tk.Label(
            self.root,
            text=title_text,
            font=("Arial", 24, "bold"),
            bg="#ffffff",      # Mismo color que el fondo del rectángulo
            fg="#4C587D",
            bd=0,
            highlightthickness=0
        )
        self.canvas.create_window(200, 100, window=title_label)

        # Mensaje descriptivo
        description_text = (
            '"Los adolescentes están expuestos a riesgos en línea como contenido inapropiado, '
            "adicción a pantallas y ciberacoso. SafeWeb busca dar a los padres herramientas "
            'para un uso seguro de internet."'
        )

        # Fondo con esquinas redondeadas (dibujado en Canvas)
        rect_x = 60
        rect_y = 170
        rect_width = 280
        rect_height = 130
        radius = 30  # Radio de las esquinas redondeadas

        self.rounded_rectangle(self.canvas, rect_x, rect_y, rect_x + rect_width, rect_y + rect_height, radius=radius, fill="#ffffff", outline="#dddddd", width=1)

        # Label encima del rectángulo redondeado
        description_label = tk.Label(
            self.root,
            text=description_text,
            wraplength=260,
            justify="center",
            font=("Arial", 12),
            bg="#ffffff",
            fg="#000000",
            highlightthickness=0
        )
        self.canvas.create_window(200, rect_y + rect_height // 2, window=description_label)  # Centrado dentro del rectángulo

        # Botón de inicio de sesión
        login_button = tk.Button(
            self.root,
            text="Iniciar Sesión",
            command=self.login,
            bg="#788AB2",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            padx=20,
            pady=8,
            bd=0,
            width=15
        )
        self.canvas.create_window(200, 500, window=login_button)

        # Vincular la tecla Enter al login
        self.root.bind('<Return>', lambda event: self.login())
        self.entry_user.bind('<Return>', lambda event: self.login())
        self.entry_pass.bind('<Return>', lambda event: self.login())

    def rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        """Dibuja un rectángulo con esquinas redondeadas en un Canvas."""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
            x1 + radius, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def on_entry_click(self, event):
        """Borra el texto predeterminado cuando el usuario hace clic."""
        widget = event.widget
        if widget.get() == widget.default_text:
            widget.delete(0, "end")
            widget.config(fg="#000000")  # Color del texto al escribir
            if widget == self.entry_pass:
                widget.config(show="*")  # Ocultar contraseña después de borrar placeholder


    def on_focus_out(self, event):
        """Restaura el texto predeterminado si el campo está vacío."""
        widget = event.widget
        if widget.get() == "":
            widget.insert(0, widget.default_text)
            widget.config(fg="grey")  # Color del placeholder
            if widget == self.entry_pass:
                widget.config(show="")  # Mostrar texto plano mientras está el placeholder

    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        width = 400
        height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Advertencia", "Por favor completa ambos campos.")
            return

        if db_manager.validate_user(username, password):
            self.root.destroy()
            from main import AppController
            app = AppController()
            app.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")