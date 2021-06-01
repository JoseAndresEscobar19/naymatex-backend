from django.urls import path, include
from rest_framework import routers
from knox import views as knox_views
from .views import *

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('registrarse/', RegistrarAPI.as_view(), name='regitrarse'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path("test/", EmpleadoAPI.as_view(), name="empleado_info"),
    path("validate/", TokenValidatorAPI.as_view(), name="validate_token")
]
