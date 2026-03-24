from django.db import models


# =============================================================================
# MODELO: CLIENTE (Prestamo)
# =============================================================================
# Almacena la informacion principal de un prestamo.
# Los campos monetarios se guardan como CharField (string) para mantener
# compatibilidad con el formato del frontend (ej: "1000000").
# =============================================================================

class Cliente(models.Model):
    # --- Datos basicos del cliente y prestamo (ya existian) ---
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

    # --- Campos nuevos para ClientesTestMejorado ---
    prestamo_sin_cronograma = models.BooleanField(
        default=False,
        help_text="True si el prestamo no genera cuotas individuales"
    )
    estado = models.CharField(
        max_length=20,
        choices=[('vigente', 'Vigente'), ('pagado', 'Pagado'), ('perdido', 'Perdido')],
        default='vigente',
        help_text="Estado actual del credito"
    )
    total_pagado_cuotas_sin_cronograma = models.CharField(
        max_length=100,
        default='0',
        help_text="Acumulado de pagos en modo sin cronograma"
    )
    interes_acumulado = models.CharField(
        max_length=100,
        default='0',
        help_text="Suma de todos los pagos de interes registrados"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.numero_tarjeta}"


# =============================================================================
# MODELO: CUOTA
# =============================================================================
# Cada cuota individual de un prestamo.
# Se relaciona con Cliente via ForeignKey (cascade delete).
# =============================================================================

class Cuota(models.Model):
    cliente     = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="cuotas")
    numero      = models.PositiveIntegerField(default=0, help_text="Numero secuencial de la cuota (1, 2, 3...)")
    fecha_pago  = models.DateField()
    valor       = models.CharField(max_length=100)
    abonado     = models.CharField(max_length=100, default='0', help_text="Monto pagado en esta cuota")
    saldo       = models.CharField(max_length=100, default='0', help_text="Monto pendiente de esta cuota")
    estado_pago = models.CharField(
        max_length=20,
        choices=[
            ('pendiente', 'Pendiente'),
            ('parcial', 'Parcial'),
            ('pagado', 'Pagado'),
        ],
        default='pendiente'
    )

    class Meta:
        ordering = ['numero']

    def __str__(self):
        return f"Cuota #{self.numero} - {self.fecha_pago} - {self.valor} - {self.estado_pago}"


# =============================================================================
# MODELO: PAGO
# =============================================================================
# Registro de cada pago realizado. Puede estar vinculado a una cuota
# o ser un pago general (interes, saldo total, sin cronograma).
# =============================================================================

class Pago(models.Model):
    TIPO_PAGO_CHOICES = [
        ('cuota', 'Pago de Cuota'),
        ('cuota_sin_cronograma', 'Pago de Cuota Sin Cronograma'),
        ('interes', 'Pago de Interés'),
        ('saldo_total', 'Pago de Saldo Total'),
        ('calculado', 'Pago Calculado'),
    ]

    cliente     = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pagos')
    cuota       = models.ForeignKey(Cuota, on_delete=models.SET_NULL, null=True, blank=True, related_name='pagos')
    tipo_pago   = models.CharField(max_length=30, choices=TIPO_PAGO_CHOICES)
    monto       = models.CharField(max_length=100)
    fecha       = models.DateField()
    descripcion = models.TextField(blank=True, default='')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.tipo_pago} - ${self.monto} - {self.fecha}"


# =============================================================================
# MODELO: PAGO INTERES
# =============================================================================
# Pagos exclusivamente de interes. Se manejan por separado porque el
# frontend los muestra en una tabla independiente y se pueden eliminar.
# =============================================================================

class PagoInteres(models.Model):
    TIPO_CHOICES = [
        ('interes', 'Interés'),
        ('liquidacion', 'Liquidación'),
    ]

    cliente     = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pagos_intereses')
    fecha       = models.DateField()
    monto       = models.CharField(max_length=100)
    tipo        = models.CharField(max_length=20, choices=TIPO_CHOICES, default='interes')
    descripcion = models.CharField(max_length=200, blank=True, default='')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PagoInteres {self.tipo} - ${self.monto} - {self.fecha}"


# =============================================================================
# MODELO: HISTORIAL EVENTO
# =============================================================================
# Log de todos los eventos que ocurren en un prestamo.
# Cada accion (crear, pagar, eliminar pago, etc) crea un registro aqui.
# =============================================================================

class HistorialEvento(models.Model):
    TIPO_CHOICES = [
        ('creacion', 'Creación'),
        ('pago', 'Pago'),
        ('eliminacion_pago', 'Eliminación de Pago'),
        ('cambio_fecha', 'Cambio de Fecha'),
        ('ampliacion', 'Ampliación'),
        ('liquidacion', 'Liquidación'),
        ('cambio_plazo', 'Cambio de Plazo'),
        ('cambio_estado', 'Cambio de Estado'),
    ]

    cliente     = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='historial')
    tipo        = models.CharField(max_length=30, choices=TIPO_CHOICES)
    titulo      = models.CharField(max_length=200)
    descripcion = models.TextField()
    monto       = models.CharField(max_length=100, null=True, blank=True)
    fecha       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.tipo} - {self.titulo}"


# =============================================================================
# MODELO: AMPLIACION
# =============================================================================
# Registro de cada ampliacion/extension de prestamo.
# Guarda los datos de la ampliacion para auditoria.
# =============================================================================

class Ampliacion(models.Model):
    cliente             = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ampliaciones')
    monto_adicional     = models.CharField(max_length=100)
    nueva_tasa          = models.CharField(max_length=100)
    nuevas_cuotas       = models.PositiveIntegerField()
    capital_anterior    = models.CharField(max_length=100)
    capital_nuevo       = models.CharField(max_length=100)
    interes_liquidacion = models.CharField(max_length=100)
    saldo_favor         = models.CharField(max_length=100)
    fecha               = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ampliacion {self.fecha} - +${self.monto_adicional}"
