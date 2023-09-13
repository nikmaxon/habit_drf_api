from rest_framework import serializers

from habit.models import PleasantHabit
from habit.validators import validate_habit_time


class PleasantHabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = PleasantHabit
        fields = '__all__'


class PleasantCreateHabitSerializer(serializers.ModelSerializer):
    duration = serializers.IntegerField(validators=[validate_habit_time])

    class Meta:
        model = PleasantHabit
        fields = '__all__'
