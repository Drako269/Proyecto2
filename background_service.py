import threading
import time
from datetime import datetime, timedelta
import psycopg2
from config import HOSTS_PATH, REDIRECT_IP
from db_manager import connect_db

def get_rules_from_db():
    """Obtiene todas las reglas desde la base de datos"""
    conn = connect_db()
    if not conn:
        return []

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        pb.url_dominio_bloqueado,
                        rb.tipo_bloqueo,
                        rb.activo,
                        rb.fecha_inicio,
                        rb.fecha_fin,
                        rb.dias_semana,
                        rb.hora_inicio,
                        rb.hora_fin
                    FROM reglas_bloqueo rb
                    JOIN paginas_bloqueadas_unicas pb ON rb.id_pagina_bloqueada_fk = pb.id_pagina_bloqueada;
                """)
                return cur.fetchall()
    except Exception as e:
        print(f"❌ Error al obtener reglas: {e}")
        return []
    finally:
        conn.close()


def update_hosts_based_on_rules():
    """Actualiza el archivo hosts según las reglas activas"""
    rules = get_rules_from_db()

    now = datetime.now()
    current_date = now.date()
    current_time = now.time()

    with open(HOSTS_PATH, 'r') as file:
        lines = file.readlines()

    new_lines = [line for line in lines if not any(rule[0] in line for rule in rules)]

    for rule in rules:
        dominio = rule[0]
        tipo_bloqueo = rule[1]
        active = rule[2]
        start_date = rule[3]
        end_date = rule[4]
        days_of_week = rule[5]
        hora_inicio = rule[6]
        hora_fin = rule[7]

        # Si no está activa, salta esta regla
        if not active:
            continue

        # Evaluar condiciones por tipo de bloqueo
        should_block = False

        if tipo_bloqueo == "periodo":
            # Bloqueo simple por página
            should_block = True

        elif tipo_bloqueo == "pagina":
            today = now.date()
            current_time = now.time()

            # Condición de fecha
            date_condition = True
            if start_date and end_date:
                date_condition = start_date <= today <= end_date
            elif start_date:
                date_condition = today >= start_date
            elif end_date:
                date_condition = today <= end_date

            # Condición de día de la semana
            day_condition = True

            if days_of_week and days_of_week.strip():
                now = datetime.now()
                current_day_name = now.strftime("%A").lower()[:3]  # ej: 'friday' → 'fri'

                # Convertir a español
                weekday_map = {
                    "mon": "lun", "tue": "mar", "wed": "mie",
                    "thu": "jue", "fri": "vie", "sat": "sab", "sun": "dom"
                }
                current_day_name = weekday_map.get(current_day_name, current_day_name)

                allowed_days = [d.strip().lower() for d in days_of_week.split(',') if d.strip()]
                
                day_condition = current_day_name in allowed_days

                print(f"Dominio: {dominio} | Días permitidos: {allowed_days} | Día actual: {current_day_name}")
            else:
                # Si days_of_week es NULL o vacío → aplica cualquier día
                day_condition = True

            # Condición de horario
            time_condition = True
            if hora_inicio and hora_fin:
                start_hour, start_minute = map(int, hora_inicio.split(':'))
                end_hour, end_minute = map(int, hora_fin.split(':'))
                start_time = time(start_hour, start_minute)
                end_time = time(end_hour, end_minute)
                time_condition = start_time <= current_time <= end_time

            should_block = date_condition and day_condition and time_condition

        # Si cumple todas las condiciones → bloquear
        if should_block:
            variants = [dominio, f"www.{dominio}"]
            for variant in variants:
                line_to_add = f"{REDIRECT_IP} {variant}\n"
                if line_to_add not in new_lines:
                    new_lines.append(line_to_add)

    # Escribir cambios
    with open(HOSTS_PATH, 'w') as file:
        file.writelines(new_lines)

# Variable global para controlar el hilo
host_updater_thread = None
stop_thread = False


def background_host_updater():
    """Actualiza el archivo hosts periódicamente"""
    try:
        while not stop_thread:
            print("🔄 Actualizando archivo hosts...")
            update_hosts_based_on_rules()
            time.sleep(60)
    except Exception as e:
        print(f"❌ Error en el hilo de actualización: {e}")


def start_background_service():
    """Inicia el hilo del fondo solo si no está corriendo"""
    global host_updater_thread

    if host_updater_thread and host_updater_thread.is_alive():
        print("ℹ️ El servicio ya está activo. No se inicia uno nuevo.")
        return

    # Iniciar el hilo por primera vez
    global stop_thread
    stop_thread = False

    global host_updater_thread
    host_updater_thread = threading.Thread(target=background_host_updater, daemon=True)
    host_updater_thread.start()
    print("✅ Servicio de actualización iniciado")

def background_host_updater_2():
    while True:
        try:
            print("🔄 Actualizando archivo hosts...")
            update_hosts_based_on_rules()
            
        except Exception as e:
            print(f"⚠️ Error al actualizar hosts: {e}")


# Llama esto al iniciar la aplicación
def start_background_service_2():
    thread = threading.Thread(target=background_host_updater_2, daemon=True)
    thread.start()