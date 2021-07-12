from django.contrib.auth import login
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from .serializers import *
from .models import *

# API


class RegistrarAPI(generics.GenericAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegistrarSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def get_post_response_data(self, request, token, instance):
        data = super().get_post_response_data(request, token, instance)
        try:
            empleado = Empleado.objects.get(usuario=request.user)
            empleado_serializer = EmpleadoSerializer(empleado).data
            data['empleado'] = empleado_serializer
            data['user']['is_gerente'] = request.user.groups.filter(
                name='Gerente').exists()
        except Empleado.DoesNotExist:
            print("No existe empleado con el usuario enviado.")
        return data

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_active:
            return Response({
                "detail": 'Usuario deshabilitado. Contácte Administración'
            }, status=status.HTTP_423_LOCKED)
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class EmpleadoAPI(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        empleado = Empleado.objects.get(usuario=request.user)
        return Response(EmpleadoSerializer(empleado).data)


class TokenValidatorAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({
            "detail": request.user.is_authenticated
        })
