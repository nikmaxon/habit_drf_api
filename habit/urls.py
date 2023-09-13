from django.urls import path

from habit.apps import HabitConfig
from habit.views.pleasant_habit import PleasantHabitListAPIView, PleasantHabitCreateAPIView, \
    PleasantHabitRetrieveAPIView, PleasantHabitDestroyAPIView, PleasantHabitUpdateAPIView, \
    PleasantHabitPublishedListAPIView
from habit.views.unpleasant_habit import UnpleasantHabitListAPIView, UnpleasantHabitCreateAPIView, \
    UnpleasantHabitRetrieveAPIView, UnpleasantHabitUpdateAPIView, UnpleasantHabitDestroyAPIView, \
    UnpleasantHabitPublishedListAPIView

app_name = HabitConfig.name

urlpatterns = [
    # приятные привычки
    path('pleasant_habit/', PleasantHabitListAPIView.as_view(), name='p_habit_list'),
    path('pleasant_habit/public_habits/', PleasantHabitPublishedListAPIView.as_view(), name='p_habit_public_list'),
    path('pleasant_habit/create/', PleasantHabitCreateAPIView.as_view(), name='p_habit_create'),
    path('pleasant_habit/<int:pk>/detail/', PleasantHabitRetrieveAPIView.as_view(), name='p_habit_detail'),
    path('pleasant_habit/<int:pk>/update/', PleasantHabitUpdateAPIView.as_view(), name='p_habit_update'),
    path('pleasant_habit/<int:pk>/delete/', PleasantHabitDestroyAPIView.as_view(), name='p_habit_delete'),

    # неприятные привычки
    path('unpleasant_habit/', UnpleasantHabitListAPIView.as_view(), name='up_habit_list'),
    path('unpleasant_habit/public_habits/', UnpleasantHabitPublishedListAPIView.as_view(), name='up_habit_public_list'),
    path('unpleasant_habit/create/', UnpleasantHabitCreateAPIView.as_view(), name='up_habit_create'),
    path('unpleasant_habit/<int:pk>/detail/', UnpleasantHabitRetrieveAPIView.as_view(), name='up_habit_detail'),
    path('unpleasant_habit/<int:pk>/update/', UnpleasantHabitUpdateAPIView.as_view(), name='up_habit_update'),
    path('unpleasant_habit/<int:pk>/delete/', UnpleasantHabitDestroyAPIView.as_view(), name='up_habit_delete'),
]
