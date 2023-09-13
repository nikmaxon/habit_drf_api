from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from habit.models import UnpleasantHabit
from habit.paginators import HabitPagination
from habit.permissions import IsOwner
from habit.serializers.unpleasant_habit import UnpleasantHabitCreateSerializer, UnpleasantHabitSerializer
from habit.tasks import unpleasant_habit_notice


class UnpleasantHabitPublishedListAPIView(ListAPIView):
    pagination_class = HabitPagination
    serializer_class = UnpleasantHabitSerializer
    queryset = UnpleasantHabit.objects.filter(is_published=True)
    permission_classes = [IsAuthenticated]


class UnpleasantHabitListAPIView(ListAPIView):
    pagination_class = HabitPagination
    serializer_class = UnpleasantHabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UnpleasantHabit.objects.filter(user=self.request.user)


class UnpleasantHabitCreateAPIView(CreateAPIView):
    serializer_class = UnpleasantHabitCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        new_habit = serializer.save()
        unpleasant_habit_notice.delay(new_habit.id)


class UnpleasantHabitRetrieveAPIView(RetrieveAPIView):
    serializer_class = UnpleasantHabitSerializer
    queryset = UnpleasantHabit.objects.all()
    permission_classes = [IsAuthenticated]


class UnpleasantHabitDestroyAPIView(DestroyAPIView):
    queryset = UnpleasantHabit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class UnpleasantHabitUpdateAPIView(UpdateAPIView):
    serializer_class = UnpleasantHabitSerializer
    queryset = UnpleasantHabit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
