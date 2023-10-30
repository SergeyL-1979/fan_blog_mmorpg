from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# from accounts.models import User


class Category(models.Model):
    """ Категория """
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return '{}'.format(self.name)


class Ad(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='AdCategory')
    title = models.CharField(max_length=255)
    # description = RichTextField()
    description = RichTextUploadingField()
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def list_category(self):
        list_of_category = [category.name for category in self.category.all()]
        return list_of_category

    def preview(self):
        return self.description[:125] + '...'

    " Добавим абсолютный путь чтобы после создания нас перебрасывало на главную страницу "
    def get_absolute_url(self):
        # return reverse('mmorpg:ads_detail', kwargs={"slug": self.slug})
        return reverse('mmorpg:ads_detail', kwargs={"pk": self.pk})  # возможен переход по id статьи\новости

    def __str__(self):
        return '{}'.format(self.title)


class AdCategory(models.Model):
    """ Добавить объявление в категорию """
    ad_category = models.ForeignKey(Ad, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.category.name)


class Respond(models.Model):
    """ Отклики на объявления """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ad_post = models.ForeignKey(Ad, on_delete=models.CASCADE)
    content = models.TextField()
    approved = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    @property
    def ad_title(self):
        return self.ad_post.title
