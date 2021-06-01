from rest_framework import permissions, viewsets
from .serializers import *
from .models import *

# Create your views here.


class ClienteView(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Cliente.objects.all()
