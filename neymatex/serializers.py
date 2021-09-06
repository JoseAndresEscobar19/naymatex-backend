from neymatex.utils import pdf_orden, print_file
from rest_framework import serializers
from .models import *
from backend.settings import env


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
        fields = ['id', 'codigo', 'estado', 'imagen', 'detalles']


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
    num_ventas = serializers.IntegerField(default=0)
    dinero_ventas = serializers.DecimalField(
        max_digits=12, decimal_places=2, default=0.00)
    categoria = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='nombre'
    )

    class Meta:
        model = Producto
        fields = '__all__'


class DetalleOrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleOrden
        fields = ["producto", "cantidad_metro", "valor_metro", "valor_total"]


class OrdenSerializer(serializers.ModelSerializer):
    detalles = DetalleOrdenSerializer(many=True)
    estado_display = serializers.CharField(
        source='get_estado_display', required=False)
    fecha_pagado = serializers.DateTimeField(required=False)
    fecha_despachado = serializers.DateTimeField(required=False)

    class Meta:
        model = Orden
        fields = ["id", "codigo", "created_at", "fecha_pagado", "fecha_despachado", "estado", "estado_display", "cliente",
                  "cliente_referencial", "empleado", "subtotal", "iva", "descuento", "valor_total",  "detalles"]

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        orden = Orden.objects.create(**validated_data)
        pre = str(orden.pk)
        sec = '0'*(9-len(pre))+pre
        orden.codigo = sec
        for producto in detalles_data:
            DetalleOrden.objects.create(orden=orden, **producto)
        orden.save()
        if env('USE_SQLITE') != "True":
            rutas = pdf_orden(orden)
            print_file(rutas[0])
        return orden


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'title', 'body', 'imagen', 'created_at']
