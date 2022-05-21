from rest_framework import serializers

from prize.models import Prize, PrizeRequest


class PrizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prize
        fields = '__all__'


class PrizeRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrizeRequest
        fields = '__all__'


class PrizeRequestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrizeRequest
        fields = ('prize',)


class PrizeRequestUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrizeRequest
        fields = ('state',)
