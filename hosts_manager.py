# hosts_manager.py

from config import HOSTS_PATH, REDIRECT_IP

def get_variants(website):
    website = website.strip().lower()
    website = website.replace("http://", "").replace("https://",  "").strip("/")
    parts = website.split('.')
    if len(parts) >= 2:
        domain = '.'.join(parts[-2:])
    else:
        domain = website
    return [
        domain,
        f"www.{domain}"
    ]

def block_website(website):
    variants = get_variants(website)
    blocked = []

    print(f"🔍 Intentando bloquear: {variants}")
    try:
        with open(HOSTS_PATH, 'r+') as file:
            content = file.read()

            for variant in variants:
                line_to_add = f"{REDIRECT_IP} {variant}"
                if variant in content:
                    print(f"⚠️ Ya bloqueado: {variant}")
                    continue
                file.write(line_to_add + "\n")
                print(f"✅ Bloqueado: {line_to_add}")
                blocked.append(variant)
    except PermissionError:
        print("❌ Error: No tienes permisos para modificar el archivo hosts.")
    except Exception as e:
        print(f"❌ Error al modificar hosts: {e}")

    return blocked

def unblock_website(website):
    removed = []

    try:
        with open(HOSTS_PATH, 'r') as file:
            lines = file.readlines()

        with open(HOSTS_PATH, 'w') as file:
            for line in lines:
                if website in line:
                    removed.append(line.strip())
                    continue
                file.write(line)
        return removed
    except Exception as e:
        print(f"❌ Error al desbloquear sitio: {e}")
        return []
    
def normalize_domain(url):
    """Limpia una URL y devuelve solo el dominio"""
    if not url:
        return None
    
    domain = url.strip()
    
    # Eliminar protocolos
    domain = domain.replace("http://", "").replace("https://",  "").replace("www.",  "")
    
    # Eliminar subdirectorios, parámetros y fragmentos
    domain = domain.split("/")[0].split("?")[0].split("#")[0]
    
    return domain