from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from advertisement.models import Advertisement
from user.models import User


class AdvertisementService:

    @staticmethod
    def watch_ad(user: User, ad_id: int):
        viewed_ads = user.get_viewed_ads()
        if viewed_ads.advertisements.filter(pk=ad_id).exists():
            raise ValidationError('Реклама уже просмотрена.')
        advertisement = get_object_or_404(Advertisement, pk=ad_id)
        with transaction.atomic():
            viewed_ads.advertisements.add(advertisement)
            user.points_amount += advertisement.cost
