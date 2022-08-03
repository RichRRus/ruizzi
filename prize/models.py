from django.db import models


class Prize(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    cost = models.FloatField(verbose_name='Стоимость')
    time_of_action = models.DurationField(blank=True, null=True, verbose_name='Время действия')
    image = models.ImageField(upload_to='prize/images', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Приз'
        verbose_name_plural = 'Призы'

    def __str__(self):
        return self.title

    def get_cost(self) -> float:
        return self.cost


class PrizeRequest(models.Model):
    class StateChoices(models.TextChoices):
        NEW = 'Новая', 'Новая'
        REJECTED = 'Отклонена', 'Отклонена'
        PROCESSING = 'В работе', 'В работе'
        DONE = 'Выполнена', 'Выполнена'

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='prize_requests',
                             verbose_name='Пользователь')
    prize = models.ForeignKey('prize.Prize', on_delete=models.CASCADE, related_name='prize_requests',
                              verbose_name='Приз')
    cost = models.FloatField(blank=True, null=True,
                             verbose_name='Стоимость приза на момент принятия заявки')
    active_up_to = models.DateTimeField(blank=True, null=True, verbose_name='Активен до')
    state = models.CharField(max_length=50, choices=StateChoices.choices, default=StateChoices.NEW,
                             verbose_name='Статус')

    class Meta:
        verbose_name = 'Заявка на получение приза'
        verbose_name_plural = 'Заявки на получение приза'

    def __str__(self):
        return f'Пользователь {self.user} оставил заявку на получение приза {self.prize}'
