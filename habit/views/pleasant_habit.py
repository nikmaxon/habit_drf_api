from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from habit.models import PleasantHabit
from habit.paginators import HabitPagination
from habit.permissions import IsOwner
from habit.serializers.pleasant_habit import PleasantCreateHabitSerializer, PleasantHabitSerializer
from habit.tasks import pleasent_habit_notice


class PleasantHabitPublishedListAPIView(ListAPIView):
    pagination_class = HabitPagination
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.filter(is_published=True)
    permission_classes = [IsAuthenticated]


class PleasantHabitListAPIView(ListAPIView):
    pagination_class = HabitPagination
    serializer_class = PleasantHabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PleasantHabit.objects.filter(user=self.request.user)


class PleasantHabitCreateAPIView(CreateAPIView):
    serializer_class = PleasantCreateHabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        new_habit = serializer.save()
        pleasent_habit_notice.delay(new_habit.id)


class PleasantHabitRetrieveAPIView(RetrieveAPIView):
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()
    permission_classes = [IsAuthenticated]


class PleasantHabitDestroyAPIView(DestroyAPIView):
    queryset = PleasantHabit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class PleasantHabitUpdateAPIView(UpdateAPIView):
    serializer_class = PleasantHabitSerializer
    queryset = PleasantHabit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
