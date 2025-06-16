# rule_engine.py

from datetime import datetime, time

def should_block_based_on_rule(rule):
    """
    Evalúa si una regla debe activarse ahora basándose en:
        - Fecha inicio/fin
        - Días de la semana
        - Hora inicio/fin
    """
    now = datetime.now()
    current_time = now.time()

    # Desempaquetar datos de la regla
    (
        id_regla,
        page_id,
        dominio,
        tipo_bloqueo,
        fecha_inicio,
        fecha_fin,
        dias_semana,
        hora_inicio,
        hora_fin,
        activo
    ) = rule

    if not activo:
        return False  # Regla desactivada

    # 1. Validar rango de fechas
    if fecha_inicio and now.date() < fecha_inicio:
        return False
    if fecha_fin and now.date() > fecha_fin:
        return False

    # 2. Validar días de la semana
    current_weekday = now.strftime("%a").lower()[:3]  # lun, mar, ..., dom
    if dias_semana:
        dias_list = dias_semana.split(',')
        if current_weekday not in dias_list:
            return False

    # 3. Validar rango horario
    if hora_inicio and hora_fin:
        start_hour, start_minute = map(int, hora_inicio.split(':'))
        end_hour, end_minute = map(int, hora_fin.split(':'))
        start_time = time(start_hour, start_minute)
        end_time = time(end_hour, end_minute)

        if not (start_time <= current_time <= end_time):
            return False

    # Si pasó todas las condiciones → Bloquear
    return True