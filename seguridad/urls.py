from django.urls import path
from .views import *
from . import apps

app_name = apps.SeguridadConfig.name
urlpatterns = [
    path("login/", login_user, name="login_admin"),
    path("logout/", logout_user, name="logout_admin"),

    # empleados
    path('empleados/', ListarEmpleados.as_view(), name='listar'),
    path('empleados/agregar/', CrearEmpleado.as_view(), name='agregar'),
    path('empleados/editar/<pk>/', EditarEmpleado.as_view(), name='editar'),
    path('empleados/eliminar/<pk>/', empleado_confirmar_eliminacion,
         name='eliminar'),
    path('empleados/activar/<pk>/', empleado_confirmar_activar,
         name='activar'),

]
