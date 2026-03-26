from rest_framework import serializers
from clientes.models import Cliente, Cuota, Pago, PagoInteres, HistorialEvento, Ampliacion, Nota


# =============================================================================
# SERIALIZERS EXISTENTES (no se modifican)
# =============================================================================

class CuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuota
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    cuotas = CuotaSerializer(many=True, read_only=True)  # Relación inversa

    class Meta:
        model = Cliente
        fields = '__all__'


# =============================================================================
# SERIALIZERS NUEVOS PARA v2
# =============================================================================

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'


class PagoInteresSerializer(serializers.ModelSerializer):
    class Meta:
        model = PagoInteres
        fields = '__all__'


class HistorialEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialEvento
        fields = '__all__'


class AmpliacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ampliacion
        fields = '__all__'


class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = '__all__'


# =============================================================================
# SERIALIZER DE DETALLE COMPLETO
# =============================================================================
# Anida TODA la informacion de un prestamo en una sola respuesta:
# cliente + cuotas + pagos + pagos de interes + historial + ampliaciones
# =============================================================================

class ClienteDetalleCompletoSerializer(serializers.ModelSerializer):
    cuotas           = CuotaSerializer(many=True, read_only=True)
    pagos            = PagoSerializer(many=True, read_only=True)
    pagos_intereses  = PagoInteresSerializer(many=True, read_only=True)
    historial        = HistorialEventoSerializer(many=True, read_only=True)
    ampliaciones     = AmpliacionSerializer(many=True, read_only=True)
    notas            = NotaSerializer(many=True, read_only=True)

    class Meta:
        model = Cliente
        fields = '__all__'
