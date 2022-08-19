from django.contrib import admin
from django.contrib import messages
from rest_framework.exceptions import ValidationError

from prize import models
from prize.services import PrizeRequestService


@admin.register(models.Prize)
class PrizeAdmin(admin.ModelAdmin):
    ...


@admin.register(models.PrizeRequest)
class PrizeRequestAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'prize',
        'state',
    )
    readonly_fields = (
        'user',
        'prize',
        'cost',
        'state',
    )
    actions = ['reject_requests', 'accept_requests', 'done_requests']
    action_messages = {
        PrizeRequestService.reject_request: 'отклонено',
        PrizeRequestService.accept_request: 'принято',
        PrizeRequestService.done_request: 'выполнено',
    }

    def process_requests(
            self,
            action,
            queryset,
            request
    ):
        success_count = 0
        failed_ids = list()
        for user_request in queryset:
            try:
                action(user_request.pk)
                success_count += 1
            except ValidationError:
                failed_ids.append(f'№{user_request.pk}')
        self.message_user(request, f'{success_count} заявок было {self.action_messages.get(action)}', messages.SUCCESS)
        if failed_ids:
            self.message_user(
                request,
                f'Заявки со следующими номерами не могут быть обработаны: {", ".join(failed_ids)}',
                messages.WARNING
            )

    @admin.action(description='Отклонить заявки')
    def reject_requests(self, request, queryset):
        self.process_requests(
            action=PrizeRequestService.reject_request,
            queryset=queryset,
            request=request
        )

    @admin.action(description='Принять заявки')
    def accept_requests(self, request, queryset):
        self.process_requests(
            action=PrizeRequestService.accept_request,
            queryset=queryset,
            request=request
        )

    @admin.action(description='Выполнить заявки')
    def done_requests(self, request, queryset):
        self.process_requests(
            action=PrizeRequestService.done_request,
            queryset=queryset,
            request=request
        )
