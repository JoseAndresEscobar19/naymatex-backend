from django.db.models import fields
from rest_framework import serializers
from .models import Orden, UserDetails, Cliente, Empleado, Producto, Categoria, TipoCategoria


class DetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('id', 'cedula', 'nombres', 'apellidos',
                  'telefono', 'telefono2', 'direccion', 'sexo')


class ClienteSerializer(serializers.ModelSerializer):
    detalles = DetalleSerializer()

    class Meta:
        model = Cliente
        fields = ['id', 'codigo', 'estado', 'monto_credito', 'detalles']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        detalles = UserDetails.objects.create(**detalles_data)
        cliente = Cliente.objects.create(detalles=detalles, **validated_data)
        return cliente


class EmpleadoSerializer(serializers.ModelSerializer):
    detalles = DetalleSerializer()

    class Meta:
        model = Empleado
        fields = ['id', 'codigo', 'estado', 'detalles']


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'codigo', 'nombre']


class TipoCategoriaSerializer(serializers.ModelSerializer):
    categorias = CategoriaSerializer(many=True)

    class Meta:
        model = TipoCategoria
        fields = ['id', 'nombre_tipo', 'categorias']


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'codigo', 'nombre', 'unidad',
                  'descripcion', 'precio', 'cantidad', 'categoria']


class OrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = "__all__"
