# firewall_manager.py

import subprocess

FIREWALL_RULE_NAME = "Bloqueo Total de Internet - Programado"

def block_internet():
    """Usa PowerShell para crear una regla que bloquee TODO el tráfico saliente"""
    try:
        # Verificar si ya existe la regla
        check_cmd = [
            'powershell.exe',
            '-Command',
            f'Get-NetFirewallRule -Name "{FIREWALL_RULE_NAME}" -ErrorAction SilentlyContinue'
        ]
        result = subprocess.run(
            check_cmd,
            capture_output=True,
            text=True,
            shell=True
        )

        if FIREWALL_RULE_NAME in result.stdout:
            print("⚠️ Regla ya existe. No es necesario crearla.")
            return True

        # Si no existe → crearla
        create_cmd = [
            'powershell.exe',
            '-Command',
            f'New-NetFirewallRule -Name "{FIREWALL_RULE_NAME}" -DisplayName "{FIREWALL_RULE_NAME}" '
            '-Direction Outbound -Action Block -Protocol Any'
        ]
        result = subprocess.run(create_cmd, capture_output=True, text=True, check=True, shell=True)

        print("✅ Regla creada:", FIREWALL_RULE_NAME)
        return True
    except subprocess.CalledProcessError as e:
        if "Ya existe un objeto con ese nombre" in e.stderr:
            print("⚠️ La regla ya existe. Ignorando duplicado.")
            return True
        else:
            print(f"❌ Error al crear la regla: {e.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error general al crear la regla de bloqueo de internet: {e}")
        return False


def unblock_internet():
    """Elimina la regla del firewall si existe"""
    try:
        # Verificar primero si la regla existe
        check_cmd = [
            'powershell.exe',
            '-Command',
            f'Get-NetFirewallRule -Name "{FIREWALL_RULE_NAME}" -ErrorAction SilentlyContinue'
        ]
        result = subprocess.run(check_cmd, capture_output=True, text=True, shell=True)

        if result.returncode != 0:
            return True  # Consideramos éxito si ya no existe

        # Si sí existe → procedemos a eliminarla
        remove_cmd = [
            'powershell.exe',
            '-Command',
            f'Remove-NetFirewallRule -Name "{FIREWALL_RULE_NAME}"'
        ]
        subprocess.run(remove_cmd, capture_output=True, text=True, check=True, shell=True)
        print("✅ Regla de firewall eliminada")
        return True
    except Exception as e:
        print("⚠️ La regla no existía o ya estaba eliminada")
        return True  # Devolvemos éxito aunque no haya nada que borrar
    
def remove_duplicate_firewall_rules():
    """Elimina reglas duplicadas con el mismo nombre"""
    try:
        cmd = [
            'powershell.exe',
            '-Command',
            f'$rules = Get-NetFirewallRule -Name "{FIREWALL_RULE_NAME}" -ErrorAction SilentlyContinue; '
            'if ($rules.Count -gt 1) { $rules | ForEach-Object { Remove-NetFirewallRule -Name $_.Name } }'
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True, shell=True)
        print("✅ Duplicados eliminados")
    except Exception as e:
        print(f"⚠️ No hubo duplicados o no había reglas")