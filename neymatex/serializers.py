from django.db.models import fields
from rest_framework import serializers
from .models import DetalleOrden, Orden, UserDetails, Cliente, Empleado, Producto, Categoria, TipoCategoria


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
        fields = ['id', 'codigo', 'nombre', 'imagen']


class TipoCategoriaSerializer(serializers.ModelSerializer):
    categorias = CategoriaSerializer(many=True)

    class Meta:
        model = TipoCategoria
        fields = ['id', 'nombre_tipo', 'categorias']


class ProductoSerializer(serializers.ModelSerializer):
    unidad = serializers.CharField(source='get_unidad_display')
    estado = serializers.CharField(source='get_estado_display')

    class Meta:
        model = Producto
        fields = ['id', 'codigo', 'nombre', 'is_active', 'estado', 'unidad',
                  'descripcion', 'precio', 'cantidad', 'imagen', 'categoria', ]


class DetalleOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleOrden
        fields = "__all__"


class OrdenSerializer(serializers.ModelSerializer):
    detalles = DetalleOrdenSerializer(many=True)

    class Meta:
        model = Orden
        fields = ["id", "codigo", "fecha", "subtotal", "iva", "descuento",
                  "valor_total", "cliente", "empleado", "detalles"]
