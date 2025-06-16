import tkinter as tk
from tkinter import messagebox

# Importaciones personalizadas
from hosts_manager import block_website, unblock_website
from db_manager import rule_exists_for_page, get_or_create_blocked_page, create_block_rule
from config import HOSTS_PATH


class BlockWebsiteFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Dominio (ej: youtube.com):").pack(pady=5)
        self.entry_website = tk.Entry(self, width=30)
        self.entry_website.pack(pady=5)

        tk.Label(self, text="Comentario (opcional):").pack(pady=5)
        self.entry_comment = tk.Entry(self, width=30)
        self.entry_comment.pack(pady=5)

        tk.Button(self, text="Bloquear Página", command=self.block_page).pack(pady=5)
        tk.Button(self, text="Desbloquear Página", command=self.unblock_page).pack(pady=5)
        tk.Button(self, text="⬅️ Regresar al Menú", command=self.go_back).pack(pady=10)

    def go_back(self):
        from menu_gui import MenuFrame
        self.controller.show_frame(MenuFrame)

    def block_page(self):
        website = self.entry_website.get().strip()
        comment = self.entry_comment.get().strip()

        if not website:
            messagebox.showwarning("Advertencia", "Por favor ingresa un dominio.")
            return

        # 1. Bloquear en hosts
        try:
            blocked_domains = block_website(website)
            if not blocked_domains:
                messagebox.showinfo("Información", "Ya existe esta regla de bloqueo.")
                return
        except PermissionError:
            messagebox.showerror("Error", "Necesitas permisos de administrador para modificar el archivo hosts.")
            return
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo bloquear el sitio:\n{e}")
            return

        for domain in blocked_domains:
            # 2. Registrar o obtener página bloqueada
            page_id = get_or_create_blocked_page(domain)
            if not page_id:
                messagebox.showerror("Error", f"No se pudo registrar {domain} en la base de datos.")
                continue

            # 3. Verificar si ya existe una regla tipo 'pagina' para este dominio
            if rule_exists_for_page(page_id):
                messagebox.showwarning("Advertencia", f"Ya hay una regla de bloqueo para '{domain}'")
                continue

            # 4. Crear la regla de bloqueo
            if not create_block_rule(page_id, rule_type="pagina"):
                messagebox.showerror("Error", f"No se pudo crear la regla de bloqueo para '{domain}'")

        messagebox.showinfo("Éxito", f"Páginas bloqueadas:\n{', '.join(blocked_domains)}")

    def unblock_page(self):
        website = self.entry_website.get().strip()
        if not website:
            messagebox.showwarning("Advertencia", "Por favor ingresa un dominio.")
            return

        try:
            removed_lines = unblock_website(website)
            if removed_lines:
                message = "\n".join(removed_lines)
                messagebox.showinfo("Éxito", f"Líneas eliminadas:\n{message}")
            else:
                messagebox.showinfo("Información", "El sitio no estaba bloqueado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo desbloquear el sitio:\n{e}")