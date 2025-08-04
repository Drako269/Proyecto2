# first_user_gui.py

import tkinter as tk
from tkinter import messagebox
from db_manager import create_user, has_users
from PIL import Image, ImageTk


class FirstUserFrame:
    def __init__(self, root):
        self.root = root
        self.root.title("SafeWeb - Registro de usuario")
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
        self.username_var = tk.Entry(
            self.root,
            font=("Arial", 12),
            bd=0,
            relief="flat",
            bg="#ffffff",
            fg="#000000",
            justify="center"
        )

        # Insertar texto inicial
        self.username_var.insert(0, "Usuario")
        self.username_var.bind("<FocusIn>", self.on_entry_click)
        self.username_var.bind("<FocusOut>", self.on_focus_out)

        # Guardamos el valor original como atributo del widget
        self.username_var.default_text = "Usuario"

        self.canvas.create_window(200, 360, window=self.username_var, width=250)

        # Campo de contraseña con placeholder
        self.password_var = tk.Entry(
            self.root,
            font=("Arial", 12),
            bd=0,
            relief="flat",
            bg="#ffffff",
            fg="#000000",
            justify="center"
        )

        self.password_var.insert(0, "Contraseña")
        self.password_var.bind("<FocusIn>", self.on_entry_click)
        self.password_var.bind("<FocusOut>", self.on_focus_out)
        self.password_var.default_text = "Contraseña"
        self.password_var.config(show="")  # Mostrar texto normal hasta que se escriba

        self.canvas.create_window(200, 430, window=self.password_var, width=250)

        # Título del aplicativo
        title_text = "Registro de Usuario"

        # Medidas del rectángulo redondeado (ajustables)
        rect_x = 40  # Posición X inicial
        rect_y = 75   # Posición Y inicial
        rect_width = 320  # Ancho del rectángulo
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
            '"Esta es una herramienta que tiene la finalidad de ayudar a los padres a '
            'gestionar el consumo de internet que tienen sus hijos y ser seguro. '
            'Para este fin se le pide al padre responsable crear un usuario y una contraseña."'
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
            text="Registrar Usuario",
            command=self.register_user,
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
        self.root.bind('<Return>', lambda event: self.register_user())
        self.username_var.bind('<Return>', lambda event: self.register_user())
        self.password_var.bind('<Return>', lambda event: self.register_user())

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
            if widget == self.password_var:
                widget.config(show="*")  # Ocultar contraseña después de borrar placeholder


    def on_focus_out(self, event):
        """Restaura el texto predeterminado si el campo está vacío."""
        widget = event.widget
        if widget.get() == "":
            widget.insert(0, widget.default_text)
            widget.config(fg="grey")  # Color del placeholder
            if widget == self.password_var:
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

    def register_user(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if not username or not password:
            messagebox.showwarning("Advertencia", "Por favor completa ambos campos.")
            return

        success = create_user(username, password)
        if success:
            messagebox.showinfo("Éxito", "Usuario creado correctamente.")
            self.root.destroy()
            from auth_gui import LoginApp
            root = tk.Tk()
            app = LoginApp(root)
            
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario.")