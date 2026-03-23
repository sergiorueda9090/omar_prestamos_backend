"""
Funciones de calculo para prestamos.
Portar de loanCalculations.js a Python.
Misma logica, mismos resultados.
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# =============================================================================
# CALCULAR INTERES SIMPLE
# =============================================================================
# Formula: interes = capital * (tasa/100) * meses
# El interes se calcula sobre MESES, no sobre numero de cuotas.
#
# Parametros:
#   capital        - Monto del prestamo (float)
#   tasa_mensual   - Tasa de interes mensual en porcentaje (float, ej: 10 = 10%)
#   num_cuotas     - Numero de cuotas a pagar (int)
#   duracion_meses - Duracion en meses (int, opcional, si no se pasa usa num_cuotas)
#
# Retorna dict con:
#   interes_mensual - Interes mensual en pesos
#   total_interes   - Total de intereses a pagar
#   valor_cuota     - Valor de cada cuota
#   saldo_total     - Capital + total de intereses
# =============================================================================

def calcular_interes_simple(capital, tasa_mensual, num_cuotas, duracion_meses=None):
    # Si no se pasa duracion_meses, se usa num_cuotas como meses
    meses_para_interes = duracion_meses if duracion_meses is not None else num_cuotas

    # Interes mensual en pesos
    interes_mensual = capital * (tasa_mensual / 100)

    # Total de intereses = interes mensual * meses
    total_interes = interes_mensual * meses_para_interes

    # Valor de cada cuota = (capital + intereses) / numero de cuotas
    valor_cuota = (capital + total_interes) / num_cuotas if num_cuotas > 0 else 0

    # Saldo total = capital + intereses
    saldo_total = capital + total_interes

    return {
        'interes_mensual': interes_mensual,
        'total_interes': total_interes,
        'valor_cuota': valor_cuota,
        'saldo_total': saldo_total,
    }


# =============================================================================
# CALCULAR NUMERO DE CUOTAS SEGUN DURACION Y TIPO
# =============================================================================
# Convierte meses a numero de cuotas segun la frecuencia de pago.
#
# Parametros:
#   duracion       - Duracion en meses (int)
#   tipo_prestamo  - Tipo: "Mensual", "Quincenal", "Semanal", "Diario"
#
# Retorna:
#   int - Numero de cuotas
# =============================================================================

def calcular_numero_cuotas(duracion, tipo_prestamo):
    meses = int(duracion)

    if tipo_prestamo == 'Mensual':
        return meses
    elif tipo_prestamo == 'Quincenal':
        return meses * 2
    elif tipo_prestamo == 'Semanal':
        return meses * 4
    elif tipo_prestamo == 'Diario':
        return meses * 30
    else:
        return meses


# =============================================================================
# CALCULAR FECHAS DE COBRO
# =============================================================================
# Genera una lista de fechas de cobro segun el tipo de prestamo.
#
# Parametros:
#   fecha_inicial  - Fecha de inicio (string "YYYY-MM-DD" o date)
#   num_cuotas     - Numero de cuotas (int)
#   tipo_prestamo  - Tipo: "Mensual", "Quincenal", "Semanal", "Diario"
#   dia_cobro      - Dia fijo de cobro (string "YYYY-MM-DD" o None)
#
# Retorna:
#   list[str] - Lista de fechas en formato "YYYY-MM-DD"
# =============================================================================

def calcular_fechas_cobro(fecha_inicial, num_cuotas, tipo_prestamo, dia_cobro=None):
    # Convertir string a date si es necesario
    if isinstance(fecha_inicial, str):
        fecha_actual = datetime.strptime(fecha_inicial, '%Y-%m-%d').date()
    else:
        fecha_actual = fecha_inicial

    # Extraer dia fijo si se paso dia_cobro
    dia_fijo = None
    if dia_cobro:
        if isinstance(dia_cobro, str):
            dia_fijo = datetime.strptime(dia_cobro, '%Y-%m-%d').date().day
        else:
            dia_fijo = dia_cobro.day

    fechas = []

    for i in range(num_cuotas):
        if tipo_prestamo == 'Mensual':
            fecha_actual = fecha_actual + relativedelta(months=1)
            # Si hay dia fijo, ajustar al dia indicado
            if dia_fijo:
                try:
                    fecha_actual = fecha_actual.replace(day=dia_fijo)
                except ValueError:
                    # Si el dia no existe en el mes (ej: 31 en febrero), usar ultimo dia
                    pass
        elif tipo_prestamo == 'Quincenal':
            fecha_actual = fecha_actual + timedelta(days=15)
        elif tipo_prestamo == 'Semanal':
            fecha_actual = fecha_actual + timedelta(days=7)
        elif tipo_prestamo == 'Diario':
            fecha_actual = fecha_actual + timedelta(days=1)
        else:
            fecha_actual = fecha_actual + relativedelta(months=1)

        fechas.append(fecha_actual.strftime('%Y-%m-%d'))

    return fechas


# =============================================================================
# APLICAR SALDO A FAVOR EN CUOTAS
# =============================================================================
# Distribuye un saldo a favor en las primeras cuotas de un cronograma nuevo.
# Las cuotas se pasan como lista de dicts (no queryset).
#
# Parametros:
#   cuotas_lista - Lista de dicts con keys: numero, fecha_pago, valor
#   saldo_favor  - Monto del saldo a favor (float)
#
# Retorna:
#   list[dict] - Lista de cuotas con abonado, saldo y estado_pago actualizados
# =============================================================================

def aplicar_saldo_favor(cuotas_lista, saldo_favor):
    saldo_restante = saldo_favor

    resultado = []
    for cuota in cuotas_lista:
        valor_cuota = float(cuota['valor'])

        if saldo_restante <= 0:
            # No hay mas saldo a favor, cuota queda pendiente
            resultado.append({
                **cuota,
                'estado_pago': 'pendiente',
                'abonado': '0',
                'saldo': str(int(valor_cuota)),
            })
        elif saldo_restante >= valor_cuota:
            # Saldo cubre toda la cuota
            saldo_restante -= valor_cuota
            resultado.append({
                **cuota,
                'estado_pago': 'pagado',
                'abonado': str(int(valor_cuota)),
                'saldo': '0',
            })
        else:
            # Saldo cubre parcialmente
            saldo_pendiente = valor_cuota - saldo_restante
            resultado.append({
                **cuota,
                'estado_pago': 'parcial',
                'abonado': str(int(saldo_restante)),
                'saldo': str(int(saldo_pendiente)),
            })
            saldo_restante = 0

    return resultado


# =============================================================================
# DISTRIBUIR PAGO EN CUOTAS
# =============================================================================
# Distribuye un monto de pago entre las cuotas pendientes en orden.
# Trabaja con un queryset de Cuota (modelo Django).
#
# Parametros:
#   cuotas_queryset - QuerySet de Cuota ordenado por 'numero'
#   monto           - Monto a distribuir (float)
#
# Retorna:
#   list[dict] - Lista con info de cada cuota afectada:
#     { cuota_id, numero, abonar, saldo_antes, saldo_despues, estado }
# =============================================================================

def distribuir_pago_en_cuotas(cuotas_queryset, monto):
    monto_restante = float(monto)
    distribucion = []

    # Recorrer cuotas en orden, solo las que tienen saldo pendiente
    for cuota in cuotas_queryset.order_by('numero'):
        if monto_restante <= 0:
            break

        saldo_cuota = float(cuota.saldo) if cuota.saldo else float(cuota.valor)

        # Saltar cuotas ya pagadas completamente
        if saldo_cuota <= 0 or cuota.estado_pago == 'pagado':
            continue

        if monto_restante >= saldo_cuota:
            # El pago cubre toda la cuota
            distribucion.append({
                'cuota_id': cuota.id,
                'numero': cuota.numero,
                'abonar': saldo_cuota,
                'saldo_antes': saldo_cuota,
                'saldo_despues': 0,
                'estado': 'pagado',
            })
            monto_restante -= saldo_cuota

            # Actualizar cuota en DB
            cuota.abonado = str(int(float(cuota.valor)))
            cuota.saldo = '0'
            cuota.estado_pago = 'pagado'
            cuota.save()
        else:
            # El pago cubre parcialmente
            nuevo_abonado = float(cuota.abonado or '0') + monto_restante
            nuevo_saldo = saldo_cuota - monto_restante

            distribucion.append({
                'cuota_id': cuota.id,
                'numero': cuota.numero,
                'abonar': monto_restante,
                'saldo_antes': saldo_cuota,
                'saldo_despues': nuevo_saldo,
                'estado': 'parcial',
            })

            # Actualizar cuota en DB
            cuota.abonado = str(int(nuevo_abonado))
            cuota.saldo = str(int(nuevo_saldo))
            cuota.estado_pago = 'parcial'
            cuota.save()

            monto_restante = 0

    return distribucion


# =============================================================================
# FORMATEAR NUMERO A STRING (estilo colombiano)
# =============================================================================
# Ejemplo: 1000000 -> "1.000.000"
# =============================================================================

def format_money(value):
    try:
        num = int(float(value))
        return f"{num:,}".replace(",", ".")
    except (ValueError, TypeError):
        return "0"


# =============================================================================
# PARSEAR STRING A NUMERO
# =============================================================================
# Ejemplo: "1.000.000" -> 1000000
# =============================================================================

def parse_money(value):
    if isinstance(value, (int, float)):
        return float(value)
    if not value:
        return 0
    try:
        return float(str(value).replace('.', '').replace(',', '.'))
    except (ValueError, TypeError):
        return 0
