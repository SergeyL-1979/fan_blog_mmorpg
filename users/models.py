from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    activation_code = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Строковое отображение поста"""
        return f'{self.username}'

    def get_absolute_url(self):
        """Получить ссылку на объект"""
        return reverse('profile')
