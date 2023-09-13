from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')
    telegram_username = models.CharField(max_length=50, verbose_name='Телеграм', **NULLABLE)
    first_name = models.CharField(max_length=150, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия', **NULLABLE)
    phone = models.CharField(max_length=50, verbose_name='Номер телефона', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Фото', **NULLABLE)
    chat_id = models.CharField(max_length=20, verbose_name='Чат', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
