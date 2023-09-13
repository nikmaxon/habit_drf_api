from rest_framework import serializers


def validate_habit_time(value):
    if value > 120:
        raise serializers.ValidationError("Время привычки не может превышать 120 секунд.")
    return value
