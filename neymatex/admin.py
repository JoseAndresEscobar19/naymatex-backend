from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserDetails)
admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(TipoCategoria)
admin.site.register(Categoria)
admin.site.register(DetalleOrden)
admin.site.register(Orden)
admin.site.register(Producto)
admin.site.register(Notificacion)
