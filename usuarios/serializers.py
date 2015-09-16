from rest_framework import serializers
from .models import Direction, PedidoPeriodico, Pregunta, CustomUser


class DirectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Direction
		fields = ('id','localidad','calle','num_interior','num_exterior','codigo_postal','colonia','delegacion_municipio','user')
		read_only_fields = ('user',)

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomUser
		fields = ('id','first_name','last_name','email','cell','direction_set','pedidoperiodico_set')
		read_only_fields = ('direction_set','pedidoperiodico_set',)
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