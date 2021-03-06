from django.db import models


class Advertisement(models.Model):
    image = models.ImageField(upload_to='advertisement/images', verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    url = models.URLField(blank=True, verbose_name='Ссылка')
    cost = models.FloatField(verbose_name='Стоимость', default=1.0)

    class Meta:
        verbose_name = 'Рекламное объявление'
        verbose_name_plural = 'Рекламные объявления'

    def __str__(self):
        return f'Объявление №{self.pk}'


class ViewedAd(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='viewed_ads',
                             verbose_name='Пользователь')
    advertisements = models.ManyToManyField('advertisement.Advertisement', related_name='viewed_ads',
                                            blank=True, verbose_name='Рекламные объявления')

    class Meta:
        verbose_name = 'Просмотренные рекламные объявления'
        verbose_name_plural = 'Просмотренные рекламные объявления'

    def __str__(self):
        return f'Просмотренные рекламные объявления пользователя {self.user}'
