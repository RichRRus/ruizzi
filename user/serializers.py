from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'phone',
            'last_name',
            'first_name',
            'middle_name',
            'location',
            'is_admin',
            'is_superuser',
            'points_amount',
        )


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'phone',
            'password',
            'last_name',
            'first_name',
            'middle_name',
        )
