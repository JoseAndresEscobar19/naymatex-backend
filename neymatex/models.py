import decimal

from django.contrib.auth.models import Group, User
from django.db import models

# Create your models here.


class UserDetails(models.Model):
    class Sex(models.TextChoices):
        MAN = 'H', 'Hombre'
        WOMEN = 'M', 'Mujer'
        OTHER = 'O', 'Otro'

    cedula = models.CharField(max_length=13)
    nombres = models.CharField(max_length=24)
    apellidos = models.CharField(max_length=24)
    telefono = models.CharField(max_length=12)
    telefono2 = models.CharField(max_length=12, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    sexo = models.CharField(max_length=2, choices=Sex.choices)

    def __str__(self):
        return self.cedula + ' - ' + self.apellidos


class Empleado(models.Model):
    class Meta:
        ordering = ['-codigo']

    class Status(models.TextChoices):
        EXCELLENT = 'EX', 'Excelente'
        GOOD = 'GD', 'Bueno'
        REGULAR = 'RG', 'Regular'
        NORMAL = 'NR', 'Normal'
        BAD = 'BD', 'Malo'
    codigo = models.CharField(max_length=255, blank=True)
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="empleado")
    detalles = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    estado = models.CharField(max_length=4,
                              choices=Status.choices, default=Status.REGULAR)
    imagen = models.ImageField(upload_to='empleado/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.detalles.nombres + ' ' + self.detalles.apellidos


class Cliente(models.Model):
    class Meta:
        ordering = ['-codigo']

    class Status(models.TextChoices):
        EXCELLENT = 'EX', 'Excelente'
        GOOD = 'GD', 'Bueno'
        REGULAR = 'RG', 'Regular'
        NORMAL = 'NR', 'Normal'
        BAD = 'BD', 'Malo'
    codigo = models.CharField(max_length=255, blank=True)
    detalles = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    estado = models.CharField(max_length=4, blank=True,
                              choices=Status.choices, default=Status.REGULAR)
    monto_credito = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.detalles.nombres + ' ' + self.detalles.apellidos


class TipoCategoria(models.Model):
    nombre_tipo = models.CharField(max_length=64)

    def __str__(self):
        return self.nombre_tipo


class Categoria(models.Model):
    nombre = models.CharField(max_length=64)
    codigo = models.CharField(max_length=64, default='')
    tipo = models.ForeignKey(
        TipoCategoria, related_name="categorias", on_delete=models.SET_NULL, null=True)
    imagen = models.ImageField(upload_to='categoria/', null=True, blank=True)

    def __str__(self):
        return self.nombre + ' - ' + self.codigo


class Producto(models.Model):
    class Meta:
        ordering = ['-id']

    class Status(models.TextChoices):
        INSTOCK = 'ISK', 'En Stock'
        OUTSTOCK = 'OSK', 'Sin Stock'
        DISABLED = 'DIS', 'Deshabilitado'

    class Unidad(models.TextChoices):
        KILOS = 'KLS', 'K'
        METROS = 'MTS', 'M'
        UNIDAD = 'UND', 'U'
    codigo = models.CharField(max_length=64)
    nombre = models.CharField(max_length=255)
    alias = models.CharField(max_length=255, default='', blank=True)
    uso = models.TextField(blank=True, default='')
    composicion = models.CharField(max_length=255, default='', blank=True)
    ancho = models.FloatField(default=0.0, blank=True)
    precioMetro = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    precioMetroEspecial = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    cantidad_metro = models.PositiveIntegerField()
    cantidad_rollo = models.PositiveIntegerField(default=100000)
    total_metros = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    estado = models.CharField(max_length=4, blank=True,
                              choices=Status.choices, default=Status.INSTOCK)
    categoria = models.ManyToManyField(Categoria)
    unidad = models.CharField(
        max_length=4, choices=Unidad.choices, default=Unidad.UNIDAD)
    imagen = models.ImageField(upload_to='producto/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def reducir_stock(self, cant_metro, commit=True):
        self.total_metros -= cant_metro
        if commit:
            self.save()
        return self.total_metros

    def validar_stock(self, cant_metro):
        if self.total_metros > cant_metro:
            print("Si hay stock suficiente")
            return True
        else:
            print("No hay stock suficiente")
            return False

    def __str__(self):
        return self.codigo + " - " + self.nombre


class Orden(models.Model):
    class Meta:
        ordering = ['-created_at', '-id']

    class Status(models.TextChoices):
        NOPAG = 'NPG', 'Pendiente de Pago'
        CANCEL = 'CNC', 'Anulada'
        PAID = 'PAG', 'Pagada'
        DES = 'DES', 'Despachada'

    codigo = models.CharField(max_length=64, blank=True)
    cliente = models.ForeignKey(
        Cliente, related_name="ordenes", on_delete=models.SET_NULL, null=True)
    cliente_referencial = models.CharField(max_length=255, blank=True)
    empleado = models.ForeignKey(
        Empleado, related_name="ordenes", on_delete=models.SET_NULL, null=True)
    cajero = models.ForeignKey(
        Empleado, related_name="ordenes_pagadas", on_delete=models.SET_NULL, null=True, blank=True)
    despachador = models.ForeignKey(
        Empleado, related_name="ordenes_despachadas", on_delete=models.SET_NULL, null=True, blank=True)
    fecha_pagado = models.DateTimeField(null=True, blank=True)
    fecha_despachado = models.DateTimeField(null=True, blank=True)
    subtotal = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    valor_total = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    estado = models.CharField(
        max_length=4, choices=Status.choices, default=Status.NOPAG)
    observaciones = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archivo = models.CharField(max_length=500, blank=True)
    archivo_root = models.CharField(max_length=500, blank=True)

    def calcular_subtotales(self):
        subtotal = 0
        for item in self.detalles.all():
            subtotal += item.valor_total
        self.valor_total = subtotal
        return subtotal

    def calcular_iva(self):
        iva = self.valor_total * decimal.Decimal(0.12)
        self.iva = iva
        return iva

    def calcular_total(self):
        total = self.valor_total - self.iva
        self.subtotal = total
        return total

    def calcular_todo(self):
        self.calcular_subtotales()
        self.calcular_iva()
        self.calcular_total()
        return self.valor_total

    def validar_stock_orden(self):
        valido = True
        for detalle in self.detalles.all():
            valido = valido and detalle.validar_stock_items()
        return valido

    def reducir_stock_orden(self):
        for detalle in self.detalles.all():
            detalle.reducir_stock_items()
        return True

    def save(self, *args, **kwargs):
        self.calcular_todo()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo


class DetalleOrden(models.Model):
    orden = models.ForeignKey(
        Orden, related_name="detalles", on_delete=models.CASCADE)
    producto = models.ForeignKey(
        Producto, related_name="detalles", on_delete=models.SET_NULL, null=True)
    cantidad_metro = models.DecimalField(max_digits=7, decimal_places=2)
    valor_metro = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    valor_total = models.DecimalField(
        max_digits=7, decimal_places=2, default=0)
    cortes = models.CharField(max_length=124, blank=True)

    def __str__(self):
        return self.orden.codigo + " - " + str(self.valor_total)

    def validar_stock_items(self):
        return self.producto.validar_stock(self.cantidad_metro)

    def reducir_stock_items(self):
        return self.producto.reducir_stock(self.cantidad_metro)

    def calcular_valor_total_detalle(self):
        valor_metro = self.valor_metro*self.cantidad_metro
        self.valor_total = valor_metro
        return self.valor_total

    def save(self, *args, **kwargs):
        self.calcular_valor_total_detalle()
        return super().save(*args, **kwargs)


class Notificacion(models.Model):
    class Meta:
        ordering = ['-created_at']

    title = models.CharField(max_length=100)
    body = models.TextField()
    imagen = models.ImageField(
        upload_to='notificacion/', null=True, blank=True)
    grupo_usuarios = models.ManyToManyField(Group, blank=True)
    usuarios = models.ManyToManyField(
        User, blank=True, related_name="notificaciones")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    # @TODO Enviar notificaciones a las personas asignadas
