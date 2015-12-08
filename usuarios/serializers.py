from rest_framework import serializers
from .models import CustomUser, Direction, ScheduledOrder, Question, Rating, Inapam
from productos.serializers import ProductSerializer


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ('id', 'location', 'street', 'interior_number', 'exterior_number',
                  'postal_code', 'colony', 'delegation_municipaly', 'user', 'lat', 'lng', 'active',)
        read_only_fields = ('user',)


class ScheduledOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledOrder
        fields = ('id', 'product', 'user', 'quantity', 'period', 'days', 'times', 'date_next', 'date_ends', )
        read_only_fields = ('user', 'date_next', 'date_ends',)


class ScheduledOrderFullSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ScheduledOrder
        fields = ('id', 'product', 'user', 'quantity', 'period', 'days', 'times', 'date_next', 'date_ends')
        read_only_fields = ('user', 'date_next', 'date_ends',)


class InapamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inapam
        fields = ('id', 'user', 'inapam', 'active')
        read_only_fields = ('user',)


class UserSerializer(serializers.ModelSerializer):
    directions = DirectionSerializer(many=True, read_only=True, )
    schedules_orders = ScheduledOrderFullSerializer(many=True, read_only=True, )
    images_inapam = InapamSerializer(many=True, read_only=True, )

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'cell', 'directions', 'schedules_orders', 'inapam',
                  'images_inapam',)
        write_only_fields = ('password',)
        depth = 1


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question', 'ask', 'order')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'comment',  'rating',)
