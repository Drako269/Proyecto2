# main.py

import tkinter as tk
import traceback
from background_service import start_background_service
from network_monitor import monitor_browser_activity

print("✅ Iniciando AppController...")

class AppController(tk.Tk):
    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
            print("🚀 Ventana principal creada")

            self.title("Bloqueador Web")
            self.geometry("800x600")
            self.resizable(True, True) #MARIO

            # Frame principal para contener las vistas
            self.container = tk.Frame(self)
            self.container.pack(side="top", fill="both", expand=True)
            self.container.grid_rowconfigure(0, weight=1)
            self.container.grid_columnconfigure(0, weight=1)

            self.frames = {}

            from menu_gui import MenuFrame
            self.show_frame(MenuFrame)


        except Exception as e:
            print("❌ Error en __init__:")
            print(traceback.format_exc())

    def show_first_user(self):
        """Muestra la vista de registro inicial"""
        from first_user_gui import FirstUserFrame
        frame = FirstUserFrame(self.container, self)
        self.frames[FirstUserFrame] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(FirstUserFrame)

    def show_frame(self, frame_class):
        """Muestra una vista (frame) específica"""
        try:
            frame = self.frames.get(frame_class)
            if not frame:
                # Importación diferida para evitar ciclos
                from block_website_gui import BlockWebsiteFrame
                from blocked_websites_gui import BlockedWebsitesFrame
                from block_internet_gui import BlockInternetFrame
                from schedule_gui import ScheduleFrame
                from add_rule_edit_gui import AddRuleFrameEdit
                from menu_gui import MenuFrame  # Importamos aquí para evitar ciclos
                from first_user_gui import FirstUserFrame

                mapping = {
                    'MenuFrame': MenuFrame,
                    'BlockWebsiteFrame': BlockWebsiteFrame,
                    'BlockedWebsitesFrame': BlockedWebsitesFrame,
                    'BlockInternetFrame': BlockInternetFrame,
                    'ScheduleFrame': ScheduleFrame,
                    'AddRuleFrameEdit': AddRuleFrameEdit,
                    'FirstUserFrame': FirstUserFrame,
                }

                # Si se pasa como cadena, obtenemos la clase desde el mapeo
                if isinstance(frame_class, str):
                    frame_class = mapping.get(frame_class)

                if frame_class:
                    frame = frame_class(self.container, self)
                    frame.grid(row=0, column=0, sticky="nsew")
                    self.frames[frame_class] = frame
                else:
                    print(f"❌ No se encontró la clase {frame_class}")
                    return

            frame.tkraise()
        except Exception as e:
            print("❌ Error en show_frame:")
            print(traceback.format_exc())


# === INICIO DEL PROGRAMA ===
if __name__ == "__main__":
    import auth_gui  # Solo importamos aquí para evitar ciclos
    import first_user_gui

    start_background_service()
    root = tk.Tk()

    # Verificar si hay usuarios
    from db_manager import has_users
    if has_users():
        # Ya hay usuarios → mostrar login
        login_app = auth_gui.LoginApp(root)
    else:
        # No hay usuarios → mostrar registro inicial
        register_app = first_user_gui.FirstUserFrame(root)

    root.mainloop()