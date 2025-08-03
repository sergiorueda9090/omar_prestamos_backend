from django.db import models

class Cliente(models.Model):
    numero_tarjeta      = models.CharField(max_length=100, unique=True)
    nombre              = models.CharField(max_length=200)
    monto_prestamo      = models.CharField(max_length=100)
    porcentaje_interes  = models.CharField(max_length=100)
    duracion_prestamo   = models.PositiveIntegerField(help_text="Duración en meses")
    tipo_prestamo       = models.CharField(max_length=100)
    fecha_prestamo      = models.DateField()
    dia_cobro           = models.DateField()
    interes_mensual     = models.CharField(max_length=100)
    numero_cuotas       = models.PositiveIntegerField()
    valor_cuota         = models.CharField(max_length=100)
    total_interes_pagar = models.CharField(max_length=100)
    saldo_total_pagar   = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.numero_tarjeta}"


class Cuota(models.Model):
    cliente     = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="cuotas")
    fecha_pago  = models.DateField()
    valor       = models.CharField(max_length=100)
    estado_pago = models.CharField(
        max_length=20,
        choices=[('pendiente', 'Pendiente'), ('pagado', 'Pagado')],
        default='pendiente'
    )
    def __str__(self):
        return f"Cuota {self.fecha_pago} - {self.valor} - {self.estado_pago}"