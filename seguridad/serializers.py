from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from neymatex.models import Empleado, UserDetails
from neymatex.serializers import DetalleSerializer, EmpleadoSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class RegistrarSerializer(serializers.ModelSerializer):
    empleado = EmpleadoSerializer()
    email = serializers.CharField(required=True, validators=[
                                  UniqueValidator(queryset=User.objects.all())])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'password2', 'empleado')
        extra_kwargs = {
            'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                # {"password": _("Password fields didn't match.")} No translation for now...
                {"password": "Las contraseñas no coinciden"}
            )
        return attrs

    def create(self, validated_data):
        empleado_data = validated_data.pop('empleado')
        detalles_data = empleado_data.pop('detalles')
        user = User.objects.create(
            username=validated_data['email'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        detalles = UserDetails.objects.create(**detalles_data)
        Empleado.objects.create(
            usuario=user, detalles=detalles, **empleado_data)
        return user
