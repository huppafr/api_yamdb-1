from django.conf import settings
from rest_framework import serializers

from .models import User


class EmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        fields = (
            'email',
        )
        model = User


class CodeSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField()

    class Meta:
        fields = (
            'confirmation_code',
        )
        model = User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default=settings.USER),

    class Meta:
        fields = (
            'confirmation_code',
            'first_name',
            'last_name',
            'username',
            'email',
            'role',
            'bio',
        )
        model = User
        extra_kwargs = {
            'confirmation_code': {'write_only': True},
            'email': {'required': True},
        }
