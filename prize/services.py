import datetime

from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from prize.models import PrizeRequest, Prize
from user.models import User


class PrizeRequestService:

    @staticmethod
    def create_request(user: User, prize_id: str) -> PrizeRequest:
        prize = get_object_or_404(Prize, pk=prize_id)
        if prize.cost > user.points_amount:
            raise ValidationError('У вас недостаточно баллов.')
        user_points = user.get_points()
        with transaction.atomic():
            prize_request = PrizeRequest.objects.create(
                user=user,
                prize=prize,
                cost=prize.cost,
            )
            user_points.amount -= prize.cost
            user_points.save()
        return prize_request

    @staticmethod
    def reject_request(request_id: str) -> None:
        prize_request = get_object_or_404(PrizeRequest, pk=request_id)
        if prize_request.state == prize_request.StateChoices.REJECTED:
            raise ValidationError('Заявка уже была отклонена.')
        user_points = prize_request.user.get_points()
        with transaction.atomic():
            user_points.amount += prize_request.cost
            prize_request.state = prize_request.StateChoices.REJECTED
            user_points.save()
            prize_request.save()

    @staticmethod
    def accept_request(request_id: str) -> None:
        prize_request = get_object_or_404(PrizeRequest, pk=request_id)
        if prize_request.state != prize_request.StateChoices.NEW:
            raise ValidationError('Заявка не может быть переведена в работу, так как не находтся в статусе "Новая".')
        prize_request.state = prize_request.StateChoices.PROCESSING
        prize_request.save()

    @staticmethod
    def done_request(request_id: str) -> None:
        prize_request = get_object_or_404(PrizeRequest, pk=request_id)
        if prize_request.state != prize_request.StateChoices.PROCESSING:
            raise ValidationError('Заявка не может быть завершена, так как не находится в статусе "В работе".')
        prize_request.state = prize_request.StateChoices.DONE

        if prize_request.prize.time_of_action:
            prize_request.active_up_to = datetime.datetime.now() + prize_request.prize.time_of_action

        prize_request.save()
