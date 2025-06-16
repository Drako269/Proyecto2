# db_manager.py

import psycopg2
from config import DB_CONFIG
from tkinter import messagebox

def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos.\n{e}")
        return None

def validate_user(username, password):
    conn = connect_db()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return bool(user)
    except Exception as e:
        messagebox.showerror("Error", f"Error al validar usuario.\n{e}")
        return False
# db_manager.py mario



def get_website_history(limit=50):
    conn = connect_db()
    if not conn:
        print("❌ No se pudo conectar a la base de datos.")
        return []

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT url_visitada, dominio, fecha_hora, bloqueada, razon_bloqueo
                    FROM registros_visitas
                    ORDER BY fecha_hora DESC
                    LIMIT %s
                """, (limit,))
                return cur.fetchall()
    except Exception as e:
        print(f"❌ Error al obtener historial: {e}")
        return []
    finally:
        conn.close()

def get_or_create_blocked_page(domain):
    conn = connect_db()
    if not conn:
        print("❌ No se pudo conectar a la base de datos.")
        return None

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id_pagina_bloqueada FROM paginas_bloqueadas_unicas 
                    WHERE url_dominio_bloqueado = %s
                """, (domain,))
                result = cur.fetchone()

                if result:
                    return result[0]

                # Si no existe, lo creamos
                cur.execute("""
                    INSERT INTO paginas_bloqueadas_unicas(url_dominio_bloqueado)
                    VALUES (%s)
                    RETURNING id_pagina_bloqueada;
                """, (domain,))
                return cur.fetchone()[0]
    except Exception as e:
        print(f"❌ Error al registrar página bloqueada: {e}")
        return None
    finally:
        conn.close()

def create_block_rule(page_id, rule_type="pagina",
                      fecha_inicio=None, fecha_fin=None,
                      dias_semana=None, hora_inicio=None, hora_fin=None):
    """Crea una regla de bloqueo asociada a una página"""
    conn = connect_db()
    if not conn:
        return False

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO reglas_bloqueo(tipo_bloqueo, fecha_inicio, fecha_fin,
                                            dias_semana, hora_inicio, hora_fin, activo,
                                            id_pagina_bloqueada_fk)
                    VALUES (%s, %s, %s, %s, %s, %s, TRUE, %s)
                """, (rule_type, fecha_inicio, fecha_fin,
                      dias_semana, hora_inicio, hora_fin, page_id))
                return cur.rowcount > 0
    except Exception as e:
        print(f"❌ Error al crear regla: {e}")
        return False
    finally:
        conn.close()

def get_all_block_rules():
    conn = connect_db()
    if not conn:
        print("❌ No se pudo conectar a la base de datos.")
        return []

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        pb.id_pagina_bloqueada AS pagina_id,
                        pb.url_dominio_bloqueado AS dominio,
                        rb.tipo_bloqueo,
                        rb.fecha_inicio,
                        rb.fecha_fin,
                        rb.dias_semana,
                        rb.hora_inicio,
                        rb.hora_fin,
                        rb.activo,
                        rb.id_regla
                    FROM reglas_bloqueo rb
                    JOIN paginas_bloqueadas_unicas pb ON rb.id_pagina_bloqueada_fk = pb.id_pagina_bloqueada
                    ORDER BY pb.url_dominio_bloqueado;
                """)
                return cur.fetchall()
    except Exception as e:
        print(f"❌ Error al obtener reglas: {e}")
        return []
    finally:
        conn.close()


def toggle_rule_active_status(rule_id, active=True):
    conn = connect_db()
    if not conn:
        return False

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE reglas_bloqueo
                    SET activo = %s
                    WHERE id_regla = %s
                """, (active, rule_id))
                return cur.rowcount > 0
    except Exception as e:
        print(f"❌ Error al actualizar estado de regla: {e}")
        return False
    finally:
        conn.close()

def rule_exists_for_page(page_id):
    """Verifica si ya existe una regla igual para esa página"""
    conn = connect_db()
    if not conn:
        return False

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 1 FROM reglas_bloqueo
                    WHERE id_pagina_bloqueada_fk = %s
                    LIMIT 1;
                """, (page_id,))
                return cur.fetchone() is not None
    except Exception as e:
        print(f"❌ Error al verificar regla: {e}")
        return False
    finally:
        conn.close()

def get_active_rules():
    """Obtiene todas las reglas con activo = TRUE"""
    conn = connect_db()
    if not conn:
        return []

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        rb.id_regla,
                        pb.id_pagina_bloqueada,
                        pb.url_dominio_bloqueado,
                        rb.tipo_bloqueo,
                        rb.fecha_inicio,
                        rb.fecha_fin,
                        rb.dias_semana,
                        rb.hora_inicio,
                        rb.hora_fin,
                        rb.activo
                    FROM reglas_bloqueo rb
                    JOIN paginas_bloqueadas_unicas pb ON rb.id_pagina_bloqueada_fk = pb.id_pagina_bloqueada
                    WHERE rb.activo = TRUE;
                """)
                return cur.fetchall()
    except Exception as e:
        print(f"❌ Error al obtener reglas: {e}")
        return []
    finally:
        conn.close()