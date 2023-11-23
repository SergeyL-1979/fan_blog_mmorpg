from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Категория')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        """Получить ссылку на объект"""
        return reverse('category', kwargs={'pk': self.pk})


class Advertisement(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True, )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        """Строковое отображение поста"""
        return f'{self.title}'

    def get_absolute_url(self):
        """Получить ссылку на объект"""
        return reverse('ads_detail', kwargs={'pk': self.pk})


class Response(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    # responded_user = models.ManyToManyField(CustomUser, related_name='post_responses',)
    accepted_responses = models.ManyToManyField(CustomUser, related_name='post_accepted_responses', )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class PrivatePage(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
