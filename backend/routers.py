from rest_framework import routers
from neymatex.viewsets import *
from seguridad.viewsets import *
from django.urls import path
from knox import views as knox_views


"""
    Here are listed CRUD APIS, using Django Rest Viewsets.
    Each api is build from:
        - A model
        - A serializer class (How the model should be serialized)
        - A viewset (a generic Class to provide standard CRUD functionality through API REST for a given model )
        - A router (only a signature to expose the api)
"""

"""
 APIS Neymatex
"""
neymatex_api = routers.DefaultRouter()
neymatex_api.register(r'clientes', ClienteView, 'cliente')
neymatex_api.register(r'empleados', EmpleadoView, 'empleado')
neymatex_api.register(r'productos', ProductoView, 'producto')
neymatex_api.register(
    r'tipo-categorias', TipoCategoriaView, 'tipo_categoria')
neymatex_api.register(r'categorias', CategoriaView, 'categoria')

"""
 APIS Seguridad
"""
seguridad_api = [path('registrarse/', RegistrarAPI.as_view(), name='regitrarse'),
                 path('login/', LoginAPI.as_view(), name='login'),
                 path('logout/', knox_views.LogoutView.as_view(), name='logout'),
                 path('logoutall/', knox_views.LogoutAllView.as_view(),
                      name='logoutall'),
                 path("test/", EmpleadoAPI.as_view(), name="empleado_info"),
                 path("validate/", TokenValidatorAPI.as_view(),
                      name="validate_token")
                 ]
