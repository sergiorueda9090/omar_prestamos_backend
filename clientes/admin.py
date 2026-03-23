from django.contrib import admin
from clientes.models import Cliente, Cuota, Pago, PagoInteres, HistorialEvento, Ampliacion


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'numero_tarjeta', 'monto_prestamo', 'estado', 'created_at')
    list_filter = ('estado', 'tipo_prestamo', 'prestamo_sin_cronograma')
    search_fields = ('nombre', 'numero_tarjeta')


@admin.register(Cuota)
class CuotaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'numero', 'fecha_pago', 'valor', 'abonado', 'saldo', 'estado_pago')
    list_filter = ('estado_pago',)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tipo_pago', 'monto', 'fecha', 'created_at')
    list_filter = ('tipo_pago',)


@admin.register(PagoInteres)
class PagoInteresAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tipo', 'monto', 'fecha', 'descripcion')
    list_filter = ('tipo',)


@admin.register(HistorialEvento)
class HistorialEventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tipo', 'titulo', 'monto', 'fecha')
    list_filter = ('tipo',)


@admin.register(Ampliacion)
class AmpliacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'monto_adicional', 'nueva_tasa', 'nuevas_cuotas', 'fecha')
