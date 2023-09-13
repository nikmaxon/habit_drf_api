from django.conf import settings
from django.db import models

from users.models import NULLABLE

PERIODICITY = [
    ('EVERY DAY', 'раз в день'),
    ('EVERY OTHER DAY', 'через день'),
    ('EVERY WEEK', 'раз в неделю'),
]


class Habit(models.Model):
    """
    Базовая модель привычек.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Создатель привычки',
                             **NULLABLE)
    place = models.CharField(max_length=150, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=150, unique=True, verbose_name='Действие')
    duration = models.PositiveIntegerField(default=120, verbose_name='Длительность выполнения, с')
    is_published = models.BooleanField(default=True, verbose_name='Признак публичности привычки')


class PleasantHabit(Habit):
    """
    Модель приятной привычки
    """
    is_pleasant_habit = models.BooleanField(default=True, verbose_name='Признак приятной привычки')

    class Meta:
        verbose_name = 'Приятная привычка'
        verbose_name_plural = 'Приятные привычки'

    def __str__(self):
        return f'{self.action}, время: {self.time}, место: {self.place}, выполнить за {self.duration} секунд'


class UnpleasantHabit(Habit):
    """
    Модель неприятной привычки
    """
    pleasant_habit = models.ForeignKey(PleasantHabit, on_delete=models.CASCADE, verbose_name='Приятная привычка',
                                       **NULLABLE)
    reward = models.TextField(verbose_name='Вознаграждение', **NULLABLE)
    frequency = models.CharField(max_length=100, default='EVERY DAY', choices=PERIODICITY, verbose_name='Периодичность')

    class Meta:
        verbose_name = 'Неприятная привычка'
        verbose_name_plural = 'Неприятные привычки'

    def __str__(self):
        return f'{self.action}, время: {self.time}, место: {self.place}, выполнить за {self.duration} ' \
               f'секунд (приятное действие: {self.pleasant_habit if self.pleasant_habit else "-"})'
