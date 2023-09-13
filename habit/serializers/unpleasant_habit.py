from rest_framework import serializers

from habit.models import UnpleasantHabit, PleasantHabit
from habit.validators import validate_habit_time


class UnpleasantHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnpleasantHabit
        fields = '__all__'


class UnpleasantHabitCreateSerializer(serializers.ModelSerializer):
    duration = serializers.IntegerField(validators=[validate_habit_time])

    def validate(self, attrs):
        if 'pleasant_habit' in attrs:
            pleasant_habit_id = attrs.get('pleasant_habit').id
            pleasant_habit = PleasantHabit.objects.filter(id=pleasant_habit_id).first()
            if pleasant_habit.is_pleasant_habit is False:
                raise serializers.ValidationError(
                    "К связанным привычкам можно отнести только привычки с признаком приятной привычки.")

        if attrs.get('pleasant_habit') is None and attrs.get('reward') is None:
            raise serializers.ValidationError("Вы должны выбрать соответствующую привычку или вознаграждение ")

        if attrs.get('pleasant_habit') and attrs.get('reward'):
            raise serializers.ValidationError("Нельзя одновременно выбрать связанную привычку и вознаграждение")
        return attrs

    class Meta:
        model = UnpleasantHabit
        fields = '__all__'
