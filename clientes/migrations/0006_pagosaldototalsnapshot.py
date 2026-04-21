from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0005_nota'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagoSaldoTotalSnapshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente_data', models.JSONField(help_text='Estado del cliente antes del pago')),
                ('cuotas_data', models.JSONField(help_text='Estado de las cuotas antes del pago')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pago', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='snapshot_saldo_total', to='clientes.pago')),
            ],
        ),
    ]
