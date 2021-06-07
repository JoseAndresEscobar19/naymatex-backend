from django.urls import path
from .views import *


urlpatterns = [
    path("login/", login_user, name="login_admin"),
    path("logout/", logout_user, name="logout_admin"),
    path('empleados/', ListarEmpleados.as_view(), name='listar_empleados'),
    path('agregar-empleado/', ListarEmpleados.as_view(), name='agregar_empleado'),
    path('editar-empleado/<pk>/', ListarEmpleados.as_view(), name='editar_empleado'),
    path('ajax/load-modal-orden-fact/<pk>/', empleado_confirmar_eliminacion,
         name='empleado_confirmar_eliminacion'),
    path('eliminar-empleado/<pk>/',
         ListarEmpleados.as_view(), name='eliminar_empleado'),
]
