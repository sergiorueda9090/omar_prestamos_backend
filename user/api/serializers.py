from rest_framework import serializers
from user.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','username', 'password', 'is_superuser', 'is_active', 'created_at']
        extra_kwargs = {'password': {'write_only': True}}  # Evita que la contraseña se devuelva en la respuesta

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            is_superuser=validated_data.get('is_superuser', False),
            is_active=validated_data.get('is_active', True),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance