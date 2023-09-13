from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from habit.models import PleasantHabit, UnpleasantHabit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.maxDiff = None
        self.user = User.objects.create(
            email='test1@mail.com',
            chat_id=123
        )
        self.user.set_password('test1')

        self.another_user = User.objects.create(
            email='test2@mail.com',
            chat_id=123
        )
        self.another_user.set_password('test2')

        self.pleasant_habit = PleasantHabit.objects.create(place='TestPlace1',
                                                           time='07:00',
                                                           action='Action',
                                                           duration=100,
                                                           user=self.user)

        self.bot_public_pleasant_habit = PleasantHabit.objects.create(place='TestPlace1',
                                                                      time='07:00',
                                                                      action='Action2',
                                                                      duration=100,
                                                                      user=self.user,
                                                                      is_published=False)

        self.unpleasant_habit = UnpleasantHabit.objects.create(place='TestPlace',
                                                               time='07:00',
                                                               action='Action0',
                                                               duration=100,
                                                               reward='TestReward',
                                                               user=self.user)

        self.unpleasant_public_habit = UnpleasantHabit.objects.create(place='TestPlace',
                                                                      time='07:00',
                                                                      action='Action1',
                                                                      duration=100,
                                                                      is_published=False,
                                                                      user=self.user)

    def test_post_pleasant_habit_create(self):
        """
        Тест на создание приятной привычки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:p_habit_create'), {'place': 'TestPlace',
                                                                      'time': '21:00',
                                                                      'action': 'Action1',
                                                                      'duration': 100})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_pleasant_habit_fail_create(self):
        """
        Тест на создание приятной привычки(не выполняется условие уникальности действия)
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:p_habit_create'), {'place': 'TestPlace',
                                                                      'time': '21:00',
                                                                      'action': 'Action',
                                                                      'duration': 100})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_pleasant_habit_fail_create_1(self):
        """
        Тест на создание приятной привычки(не выполняется условие по длительности привычки)
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:p_habit_create'), {'place': 'TestPlace',
                                                                      'time': '21:00',
                                                                      'action': 'Action1',
                                                                      'duration': 130})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_pleasant_habit_1(self):
        """
        Тест на вывод списка личных привычек пользователей
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('habit:p_habit_list'))
        self.assertEqual(
            response.json(),
            {'count': 2,
             'next': None,
             'previous': None,
             'results': [
                 {'id': 3,
                  'place': 'TestPlace1',
                  'time': '07:00:00',
                  'action': 'Action',
                  'duration': 100,
                  'is_published': True,
                  'is_pleasant_habit': True,
                  'user': 3},
                 {'id': 4,
                  'place': 'TestPlace1',
                  'time': '07:00:00',
                  'action': 'Action2',
                  'duration': 100,
                  'is_published': False,
                  'is_pleasant_habit': True,
                  'user': 3}]})

    def test_list_pleasant_habit_2(self):
        """
        Тест на вывод списка привычек пользователей
        """
        self.client.force_authenticate(user=self.another_user)
        response = self.client.get(reverse('habit:p_habit_public_list'))
        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [
                 {'id': 5,
                  'place': 'TestPlace1',
                  'time': '07:00:00',
                  'action': 'Action',
                  'duration': 100,
                  'is_published': True,
                  'is_pleasant_habit': True,
                  'user': 5}]}
        )

    def test_retrieve_pleasant_habit(self):
        """
        Тестирование просмотра привычки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('habit:p_habit_detail', kwargs={'pk': self.pleasant_habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.pleasant_habit.pk)

    def test_update_pleasant_habit(self):
        """
        Тестирование редактирования привычки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('habit:p_habit_update', kwargs={'pk': self.pleasant_habit.pk}),
                                     {'place': 'UpdatePlaceTest'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 'UpdatePlaceTest')

    def test_delete_pleasant_habit(self):
        """
        Тестирование удаления привычки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('habit:p_habit_delete', kwargs={'pk': self.pleasant_habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_post_unpleasant_habit_create(self):
        """
        Тест на создание неприятной привычки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:up_habit_create'), {'place': 'TestPlace',
                                                                       'time': '21:00',
                                                                       'action': 'Action1',
                                                                       'duration': 100,
                                                                       'reward': 'Пончик'}
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_unpleasant_habit_fail_create(self):
        """
        Тест на создание неприятной привычки(не выполняется условие уникальности действия)
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:up_habit_create'), {'place': 'TestPlace',
                                                                       'time': '21:00',
                                                                       'action': 'Action0',
                                                                       'duration': 100})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_unpleasant_habit_fail_create_1(self):
        """
        Тест на создание приятной привычки(не выполняется условие по длительности привычки)
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:up_habit_create'), {'place': 'TestPlace',
                                                                       'time': '21:00',
                                                                       'action': 'Action1',
                                                                       'duration': 130})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_unpleasant_habit_fail_create_2(self):
        """
        Тестирование создания неприятной привычки
        (не выполняется условие: невозможен одновременный выбор приятной привычки и вознаграждения)
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('habit:up_habit_create'), {'place': 'TestPlace',
                                                                       'time': '21:00',
                                                                       'action': 'Action1',
                                                                       'duration': 130,
                                                                       'reward': 'TestReward',
                                                                       'pleasant_habit': 'Пончик'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_unpleasant_habit_1(self):
        """
        Тест на вывод списка личных неприятных привычек пользователей
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('habit:up_habit_list'))
        self.assertEqual(
            response.json(),
            {'count': 2,
             'next': None,
             'previous': None,
             'results': [
                 {'id': 3,
                  'place': 'TestPlace',
                  'time': '07:00:00',
                  'action': 'Action0',
                  'duration': 100,
                  'reward': 'TestReward',
                  'user': 1,
                  'frequency': 'EVERY DAY',
                  'is_published': True,
                  'pleasant_habit': None},
                 {'id': 4,
                  'place': 'TestPlace',
                  'time': '07:00:00',
                  'action': 'Action1',
                  'duration': 100,
                  'is_published': False,
                  'user': 1,
                  'frequency': 'EVERY DAY',
                  'pleasant_habit': None,
                  'reward': None,
                  }]})

    def test_list_unpleasant_habit_2(self):
        """
        Тест на вывод списка привычек пользователей
        """
        self.client.force_authenticate(user=self.another_user)
        response = self.client.get(reverse('habit:up_habit_public_list'))
        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [
                 {'id': 3,
                  'place': 'TestPlace',
                  'time': '07:00:00',
                  'action': 'Action0',
                  'duration': 100,
                  'reward': 'TestReward',
                  'user': 1,
                  'frequency': 'EVERY DAY',
                  'is_published': True,
                  'pleasant_habit': None}
             ]}
        )

    def test_retrieve_unpleasant_habit(self):
        """
        Тестирование просмотра неприятной привычки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('habit:up_habit_detail', kwargs={'pk': self.unpleasant_habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.unpleasant_habit.pk)

    def test_update_unpleasant_habit(self):
        """
        Тестирование редактирования неприятной привычки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse('habit:up_habit_update', kwargs={'pk': self.unpleasant_habit.pk}),
                                     {'place': 'UpdatePlaceTest'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['place'], 'UpdatePlaceTest')

    def test_delete_unpleasant_habit(self):
        """
        Тестирование удаления неприятной привычки
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('habit:up_habit_delete', kwargs={'pk': self.unpleasant_habit.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
