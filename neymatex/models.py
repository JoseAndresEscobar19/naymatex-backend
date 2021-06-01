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
    class Status(models.TextChoices):
        EXCELLENT = 'EX', 'Excelente'
        GOOD = 'GD', 'Bueno'
        REGULAR = 'RG', 'Regular'
        NORMAL = 'NR', 'Normal'
        BAD = 'BD', 'Malo'
    codigo = models.CharField(max_length=255, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    detalles = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    estado = models.CharField(max_length=4, blank=True,
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

    def __str__(self):
        return self.codigo + ' - ' + self.detalles.apellidos


class Notificacion(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=500)
    imagen = models.ImageField(
        upload_to='notificacion/', null=True, blank=True)
    usuario = models.ManyToManyField(Empleado, blank=True)

    def __str__(self):
        return self.title
