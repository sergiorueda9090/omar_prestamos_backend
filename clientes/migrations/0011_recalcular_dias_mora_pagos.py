# Backfill: recalcula dias_mora de los pagos historicos con la formula corregida.
#
# Antes el calculo tenia el signo invertido (fecha_pago_real - fecha_proximo_pago)
# y todos los pagos quedaban con dias_mora = 0. Como ambas fechas SI se guardaron
# (su semantica no cambio: fecha_proximo_pago = referencia/promesa,
# fecha_pago_real = vencimiento de la cuota), se puede recalcular de forma exacta:
#     dias_mora = max(0, fecha_proximo_pago - fecha_pago_real)

from django.db import migrations


def recalcular_dias_mora(apps, schema_editor):
    Pago = apps.get_model('clientes', 'Pago')
    pagos = Pago.objects.filter(
        tipo_pago='cuota',
        fecha_proximo_pago__isnull=False,
        fecha_pago_real__isnull=False,
    )
    for pago in pagos.iterator():
        dias = max(0, (pago.fecha_proximo_pago - pago.fecha_pago_real).days)
        if dias != pago.dias_mora:
            pago.dias_mora = dias
            pago.save(update_fields=['dias_mora'])


def revertir(apps, schema_editor):
    # Reversion best-effort: deja dias_mora en 0 (estado previo al fix).
    Pago = apps.get_model('clientes', 'Pago')
    Pago.objects.filter(tipo_pago='cuota').update(dias_mora=0)


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0010_alter_pago_dias_mora_alter_pago_fecha_pago_real_and_more'),
    ]

    operations = [
        migrations.RunPython(recalcular_dias_mora, revertir),
    ]
