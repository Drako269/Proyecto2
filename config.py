# config.py

import platform

# Ruta del archivo hosts dependiendo del sistema operativo
if platform.system() == "Windows":
    HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
else:
    HOSTS_PATH = "/etc/hosts"

REDIRECT_IP = "127.0.0.1"
APP_NAME = "Bloqueador de Sitios Web"
WINDOW_SIZE = "400x250"

# Configuración de PostgreSQL
DB_CONFIG = {
    'dbname': 'blocker_db',
    'user': 'postgres',
    'password': '123456',
    'host': 'localhost',
    'port': 5432
}