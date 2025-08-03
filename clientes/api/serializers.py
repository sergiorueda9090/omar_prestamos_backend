from rest_framework import serializers
from clientes.models import Cliente, Cuota

class CuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuota
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    cuotas = CuotaSerializer(many=True, read_only=True)  # Relación inversa

    class Meta:
        model = Cliente
        fields = '__all__'
