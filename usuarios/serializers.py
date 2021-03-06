# -*- encoding: utf-8 -*-
from rest_framework import serializers
from .models import CustomUser, Direction, ScheduledOrder, Question, Rating, Inapam, TokenPhone, CardConekta, Reminder
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
        fields = ('id', 'product', 'user', 'direction', 'card_conekta', 'quantity', 'period', 'days', 'times',
                  'date_next', 'date_ends',)
        read_only_fields = ('user', 'date_next', 'date_ends',)


class ScheduledOrderFullSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ScheduledOrder
        fields = ('id', 'product', 'user', 'direction', 'card_conekta', 'quantity', 'period', 'days', 'times',
                  'date_next', 'date_ends')
        read_only_fields = ('user', 'date_next', 'date_ends',)


class InapamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inapam
        fields = ('id', 'user', 'image', 'active')
        read_only_fields = ('user',)


class TokenPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenPhone
        fields = ('id', 'user', 'token', 'active', 'created',)
        read_only_fields = ('user', 'created',)


class CardConektaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardConekta
        fields = ('id', 'user', 'card', 'name', 'brand', 'last4', 'active', 'exp_year', 'exp_month', 'created',
                  'allows_payouts', 'allows_charges', 'bank_name', 'type')
        read_only_fields = ('user', 'created',)


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = (
            'id', 'user', 'title', 'message', 'time', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday',
            'sunday', 'active')
        read_only_fields = ('user',)


class UserSerializer(serializers.ModelSerializer):
    directions = DirectionSerializer(many=True, read_only=True, )
    schedules_orders = ScheduledOrderFullSerializer(many=True, read_only=True, )
    token_phone = TokenPhoneSerializer(many=True, read_only=True, )
    images_inapam = InapamSerializer(many=True, read_only=True, )
    cards = CardConektaSerializer(many=True, read_only=True)
    reminders = ReminderSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'cell', 'directions', 'schedules_orders', 'inapam',
                  'token_phone', 'images_inapam', 'cards', 'reminders')
        write_only_fields = ('password',)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question', 'ask', 'order')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'comment', 'rating',)
