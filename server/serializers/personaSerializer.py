from rest_framework import serializers

from server.models import Persona


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'

    def validate_name(self, value):
        if value[0] == '@':
            return value

        raise serializers.ValidationError("El nombre debe comenzar con @")

    def validate_age(self, value):
        if value >= 18:
            return value

        raise serializers.ValidationError("La edad debe ser mayor de 18")

    def validate(self, attrs):
        if attrs['name'][0] != '@' and attrs['age'] < 18:
            raise serializers.ValidationError(
                "Nombre de usuario incorrecto, Solo puede usar nuestro servicio usuarios mayores de 18"
            )

        return super().validate(attrs)
