from django.conf import settings
# from django.core.exceptions import ValidationError
# from django.core.validators import validate_email
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default=settings.USER)

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
            'username': {'required': True},
            'email': {'required': True},
        }

        # def validateEmail(self, email):
        #     try:
        #         validate_email(email)
        #         return True
        #     except ValidationError:
        #         return False

