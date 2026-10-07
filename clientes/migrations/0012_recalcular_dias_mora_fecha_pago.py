# Backfill: recalcula dias_mora de los pagos historicos con la formula
# corregida (ver clientes/api/views.py, registrar_pago / registrar_pago_interes).
#
# Antes: dias_mora = max(0, fecha_proximo_pago - fecha_pago_real), usando la
# promesa del cliente para el SIGUIENTE ciclo como referencia. Eso inflaba la
# mora del pago actual cada vez que se programaba una fecha de pago futura.
#
# Ahora: dias_mora = max(0, fecha - fecha_pago_real), usando la fecha real en
# que se registro el pago (columna 'fecha', siempre presente) contra el
# vencimiento original de la cuota (fecha_pago_real).

from django.db import migrations


def recalcular_dias_mora(apps, schema_editor):
    Pago = apps.get_model('clientes', 'Pago')
    pagos = Pago.objects.filter(
        tipo_pago__in=['cuota', 'interes'],
        fecha_pago_real__isnull=False,
    )
    for pago in pagos.iterator():
        dias = max(0, (pago.fecha - pago.fecha_pago_real).days)
        if dias != pago.dias_mora:
            pago.dias_mora = dias
            pago.save(update_fields=['dias_mora'])


def revertir(apps, schema_editor):
    # Reversion best-effort: recalcula con la formula anterior (fecha_proximo_pago).
    Pago = apps.get_model('clientes', 'Pago')
    pagos = Pago.objects.filter(
        tipo_pago__in=['cuota', 'interes'],
        fecha_proximo_pago__isnull=False,
        fecha_pago_real__isnull=False,
    )
    for pago in pagos.iterator():
        dias = max(0, (pago.fecha_proximo_pago - pago.fecha_pago_real).days)
        if dias != pago.dias_mora:
            pago.dias_mora = dias
            pago.save(update_fields=['dias_mora'])


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0011_recalcular_dias_mora_pagos'),
    ]

    operations = [
        migrations.RunPython(recalcular_dias_mora, revertir),
    ]
