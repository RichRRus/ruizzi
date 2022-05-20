from django.db import models


class Advertisement(models.Model):
    image = models.ImageField(upload_to='advertisement_images', verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    url = models.URLField(blank=True, verbose_name='Ссылка')
    cost = models.FloatField(verbose_name='Стоимость', default=1.0)

    class Meta:
        verbose_name = 'Рекламное объявление'
        verbose_name_plural = 'Рекламные объявления'

    def __str__(self):
        return f'Объявление №{self.pk}'
