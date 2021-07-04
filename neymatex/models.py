from django.db import models
from django.contrib.auth.models import User

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
        ordering = ['codigo']

    class Status(models.TextChoices):
        EXCELLENT = 'EX', 'Excelente'
        GOOD = 'GD', 'Bueno'
        REGULAR = 'RG', 'Regular'
        NORMAL = 'NR', 'Normal'
        BAD = 'BD', 'Malo'
    codigo = models.CharField(max_length=255, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    detalles = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    estado = models.CharField(max_length=4,
                              choices=Status.choices, default=Status.REGULAR)

    def __str__(self):
        return self.codigo + ' - ' + self.detalles.cedula + ' - ' + self.detalles.nombres


class Cliente(models.Model):
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
        max_digits=6, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.codigo + ' - ' + self.detalles.apellidos


class TipoCategoria(models.Model):
    nombre_tipo = models.CharField(max_length=64)

    def __str__(self):
        return self.nombre_tipo


class Categoria(models.Model):
    nombre = models.CharField(max_length=64)
    tipo = models.ForeignKey(
        TipoCategoria, related_name="categorias", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    class Status(models.TextChoices):
        INSTOCK = 'ISK', 'En Stock'
        OUTSTOCK = 'OSK', 'Sin Stock'
        DISABLED = 'DIs', 'Deshabilitado'
    codigo = models.CharField(max_length=64)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    cantidad = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    estado = models.CharField(max_length=4, blank=True,
                              choices=Status.choices, default=Status.INSTOCK)
    categoria = models.ManyToManyField(
        Categoria)

    def __str__(self):
        return self.codigo + " - " + self.nombre


class Orden(models.Model):
    codigo = models.CharField(max_length=64, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    empleado = models.ForeignKey(
        Empleado, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=5, decimal_places=2)
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    valor_total = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)

    def calcular_iva(self):
        iva = self.subtotal * 0.12
        self.iva = iva
        self.save()
        return iva

    def calcular_total(self):
        total = self.subtotal + self.iva - self.descuento
        self.valor_total = total
        self.save()
        return total

    def __str__(self):
        return self.codigo + " - " + self.fecha


class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(
        Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.PositiveIntegerField()
    valor_total = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)

    def calcular_total(self):
        total = self.cantidad*self.producto.precio
        self.valor_total = total
        self.save()
        return total

    def __str__(self):
        return self.orden.codigo + " - " + self.valor_total


class Notificacion(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=500)
    imagen = models.ImageField(
        upload_to='notificacion/', null=True, blank=True)
    usuario = models.ManyToManyField(Empleado, blank=True)

    def __str__(self):
        return self.title
