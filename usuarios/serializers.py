from rest_framework import serializers

from .models import Direction, Profile, PedidoPeriodico, Pregunta
from django.contrib.auth.models import User


class DirectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Direction
		fields = ('id','localidad','calle','num_interior','num_exterior','codigo_postal','colonia','delegacion_municipio','user')
		read_only_fields = ('user',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('cell','user')
        read_only_fields = ('user',)

class UserSerializer(serializers.ModelSerializer):

	cell = serializers.CharField(source='profile.cell',read_only=False)

	class Meta:
		model = User
		fields = ('id','first_name','last_name','username','cell','direction_set','pedidoperiodico_set')
		write_only_fields = ('password',)
		depth = 1

class PedidoPeriodicoSerializer(serializers.ModelSerializer):
	class Meta:
		model = PedidoPeriodico
		fields = ('id','producto','user','cantidad','periodo','lunes','martes','miercoles','jueves','viernes','sabado','domingo','fecha_entrega')
		read_only_fields = ('user',)


class PreguntaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Pregunta
		fields = ('id','pregunta','respuesta','orden')		