from .models import Direction, ScheduledOrder, CustomUser, Question, Rating, Inapam
from .serializers import DirectionSerializer, ScheduledOrderSerializer, UserSerializer, \
    QuestionSerializer, RatingSerializer, InapamSerializer
from rest_framework import viewsets


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        """
        This view should return only the user login.
        """
        user = self.request.user
        return CustomUser.objects.filter(id=user.id)


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


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()


class InapamViewSet(viewsets.ModelViewSet):
    serializer_class = InapamSerializer
    queryset = Inapam.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, inapam=self.request.data.get('inapam'))

    def get_queryset(self):
        """
        This view should return a list of all the directions
        for the currently authenticated user.
        """
        user = self.request.user
        return Inapam.objects.filter(user=user)
