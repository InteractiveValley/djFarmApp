from .models import Direction, ScheduledOrder, CustomUser, Question
from .serializers import DirectionSerializer, ScheduledOrderSerializer, UserSerializer, QuestionSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class DirectionViewSet(viewsets.ModelViewSet):
    serializer_class = DirectionSerializer
    queryset = Direction.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all the directions
        for the currently authenticated user.
        """
        user = self.request.user
        return Direction.objects.filter(user=user)


class ScheduledOrderViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduledOrderSerializer
    queryset = ScheduledOrder.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all the schedules orders
        for the currently authenticated user.
        """
        user = self.request.user
        return ScheduledOrder.objects.filter(user=user)


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
