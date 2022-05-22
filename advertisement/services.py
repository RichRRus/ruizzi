from rest_framework.generics import get_object_or_404

from advertisement.models import Advertisement
from user.models import User


class AdvertisementService:

    @staticmethod
    def watch_ad(user: User, ad_id: int):
        advertisement = get_object_or_404(Advertisement, pk=ad_id)
        viewed_ads = user.get_viewed_ads()
        viewed_ads.advertisements.add(advertisement)
