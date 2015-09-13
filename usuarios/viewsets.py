from .models import Direction, PedidoPeriodico, Pregunta
from django.contrib.auth.models import User
from .serializers import UserSerializer, DirectionSerializer, PedidoPeriodicoSerializer, PreguntaSerializer
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class DirectionViewSet(viewsets.ModelViewSet):
    serializer_class = DirectionSerializer
    queryset = Direction.objects.all()


class PedidoPeriodicoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoPeriodicoSerializer
    queryset = PedidoPeriodico.objects.all()


class PreguntaViewSet(viewsets.ModelViewSet):
    serializer_class = PreguntaSerializer
    queryset = Pregunta.objects.all()
