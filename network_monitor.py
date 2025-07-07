# network_monitor.py

import sqlite3
import shutil
import os
import time as python_time
from datetime import datetime, timedelta
from urllib.parse import urlparse

from db_manager import connect_db, log_website_visit

# Variable global para evitar duplicados
last_visited_urls = set()

def convert_chrome_time(chrome_time):
    """Convierte el tiempo de Chrome a datetime"""
    epoch_start = datetime(1601, 1, 1)
    microseconds_per_hour = 1000000 * 60 * 60
    return epoch_start + timedelta(microseconds=chrome_time)

def extract_domain(url):
    """Extrae solo el dominio principal"""
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path.split("/")[0]
    return domain.replace("www.", "").strip()

def get_chrome_history():
    """Obtiene el historial de Google Chrome"""
    history_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\History'
    temp_path = 'temp_chrome.db'

    try:
        if not os.path.exists(history_path):
            print("❌ No se encontró el historial de Chrome")
            return []

        # Copiar History para evitar bloqueos
        shutil.copy(history_path, temp_path)

        conn = sqlite3.connect(temp_path)
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM urls ORDER BY last_visit_time DESC LIMIT 50")
        rows = cursor.fetchall()
        conn.close()
        os.remove(temp_path)

        return [row[0] for row in rows]

    except Exception as e:
        print(f"⚠️ No se pudo leer el historial de Chrome: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return []

def monitor_browser_activity():
    """Monitorea y guarda automáticamente las URLs visitadas (una sola vez)"""
    global last_visited_urls
    
    urls = get_chrome_history()
    new_urls = [url for url in urls if url not in last_visited_urls]

    # Guardar nuevas URLs
    for url in new_urls:
        domain = extract_domain(url)
        success = log_website_visit(url, domain)
        if success:
            last_visited_urls.add(url)
        else:
            print(f"❌ No se pudo registrar: {url}")
