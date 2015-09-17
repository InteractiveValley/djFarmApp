from rest_framework import serializers
from .models import CustomUser, Direction, ScheduledOrder, Question


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ('id', 'location', 'street', 'interior_number', 'exterior_number',
                  'postal_code', 'colony', 'delegation_municipaly', 'user',)
        read_only_fields = ('user',)


class ScheduledOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledOrder
        fields = ('id', 'product', 'user', 'quantity', 'period', 'days', 'times', 'date_next', 'date_ends')
        read_only_fields = ('user', 'date_next', 'date_ends',)


class UserSerializer(serializers.ModelSerializer):
    directions = DirectionSerializer(many=True, read_only=True, )
    schedules_orders = ScheduledOrderSerializer(many=True, read_only=True, )

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'cell', 'directions', 'schedules_orders')
        write_only_fields = ('password',)
        depth = 1


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question', 'ask', 'order')
