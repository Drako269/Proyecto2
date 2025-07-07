import sqlite3
import shutil
import os
import time

# Conjunto global para rastrear páginas ya mostradas
visited_pages = set()

def get_chrome_history():
    history_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\History'
    temp_path = 'history_temp.db'

    # Copiar archivo History para evitar bloqueo
    shutil.copy(history_path, temp_path)

    conn = sqlite3.connect(temp_path)
    cursor = conn.cursor()
    cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10")

    new_pages = []
    for row in cursor.fetchall():
        url = row[0]
        if url not in visited_pages:
            new_pages.append(row)
            visited_pages.add(url)  # Agregar a la lista de visitados

    conn.close()
    os.remove(temp_path)

    return new_pages


while True:
    print("\n--- Historial actualizado ---")
    new_pages = get_chrome_history()
    
    if new_pages:
        for page in new_pages:
            print(page)
    else:
        print("No hay nuevas páginas visitadas.")
    
    time.sleep(10)  # Cada 10 segundos