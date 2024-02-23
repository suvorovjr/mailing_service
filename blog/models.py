from django.db import models
from users.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    slug = models.CharField(max_length=255, unique=True, verbose_name='Слаг', **NULLABLE)
    imagine = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_publish = models.BooleanField(default=True, verbose_name='Активность')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
