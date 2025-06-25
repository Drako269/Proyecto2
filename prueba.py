import win32com.client
import pythoncom
import sys

def crear_regla_firewall_win32com(nombre_regla, direccion='in', accion='allow', protocolo=6,
                                ip_local='any', ip_remota='any', puerto_local='any',
                                puerto_remoto='any', perfil=0x7, programa=None):
    """
    Versión mejorada con mejor manejo de errores
    """
    try:
        # Inicializar COM
        pythoncom.CoInitialize()
        
        # Crear instancia del administrador de firewall
        fwMgr = win32com.client.Dispatch("HNetCfg.FwMgr")
        fwPolicy = fwMgr.LocalPolicy.CurrentProfile
        
        # Verificar si la regla ya existe
        try:
            existing_rule = fwPolicy.Rules.Item(nombre_regla)
            print(f"La regla '{nombre_regla}' ya existe. Eliminándola primero...")
            fwPolicy.Rules.Remove(nombre_regla)
        except:
            pass  # La regla no existe, continuamos
        
        # Crear una nueva regla
        fwRule = win32com.client.Dispatch("HNetCfg.FWRule")
        
        # Configurar propiedades básicas
        fwRule.Name = nombre_regla
        fwRule.Description = f"Regla creada automáticamente para {nombre_regla}"
        fwRule.Enabled = True
        
        # Configurar dirección (1 = entrada, 2 = salida)
        fwRule.Direction = 1 if direccion.lower() == 'in' else 2
        
        # Configurar acción (0 = bloquear, 1 = permitir)
        fwRule.Action = 1 if accion.lower() == 'allow' else 0
        
        # Configurar protocolo
        protocol_map = {
            'tcp': 6,
            'udp': 17,
            'icmp': 1,
            'any': 256
        }
        if isinstance(protocolo, str):
            fwRule.Protocol = protocol_map.get(protocolo.lower(), 6)
        else:
            fwRule.Protocol = protocolo
        
        # Configurar direcciones IP
        fwRule.LocalAddresses = ip_local if ip_local != 'any' else '*'
        fwRule.RemoteAddresses = ip_remota if ip_remota != 'any' else '*'
        
        # Configurar puertos
        if puerto_local != 'any':
            fwRule.LocalPorts = str(puerto_local)
        if puerto_remoto != 'any':
            fwRule.RemotePorts = str(puerto_remoto)
        
        # Configurar perfil
        fwRule.Profiles = perfil
        
        # Configurar aplicación si se especifica
        if programa:
            fwRule.ApplicationName = programa
        
        # Agregar la regla al firewall
        fwPolicy.Rules.Add(fwRule)
        
        print(f"Regla '{nombre_regla}' creada exitosamente.")
        return True
        
    except pythoncom.com_error as e:
        hr, msg, exc, arg = e.args
        print(f"Error COM al crear la regla (0x{hr:x}): {msg}")
        if exc and exc[5]:  # Código de error específico
            print(f"Código de error: 0x{exc[5]:x}")
        return False
    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        return False
    finally:
        try:
            pythoncom.CoUninitialize()
        except:
            pass

# Ejemplo de uso mejorado
if __name__ == "__main__":
    # Verificar permisos de administrador
    import ctypes
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("ERROR: Este script debe ejecutarse como administrador.")
        sys.exit(1)
    
    # Ejemplo 1: Permitir HTTP
    if crear_regla_firewall_win32com(
        nombre_regla="Permitir HTTP (Python)",
        direccion="in",
        accion="allow",
        protocolo="tcp",
        puerto_local="80",
        perfil=0x7  # Todos los perfiles
    ):
        print("Regla HTTP creada con éxito")
    else:
        print("Fallo al crear regla HTTP")
    
    # Ejemplo 2: Bloquear programa
    if crear_regla_firewall_win32com(
        nombre_regla="Bloquear App Ejemplo",
        direccion="out",
        accion="block",
        programa="C:\\Path\\To\\App.exe",
        perfil=0x7
    ):
        print("Regla de bloqueo creada con éxito")
    else:
        print("Fallo al crear regla de bloqueo")