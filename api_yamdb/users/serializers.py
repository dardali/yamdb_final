import re

from django.core.validators import (MaxLengthValidator, MinLengthValidator,
                                    RegexValidator)
from rest_framework import serializers

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate_username(self, value):
        min_length = 5
        max_length = 150
        validators = [
            MinLengthValidator(min_length),
            MaxLengthValidator(max_length),
            # Добавляем проверку на соответствие паттерну
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message=('Логин содержит недопустимые символы'),
            ),
        ]

        # Применяем все валидаторы к значению поля username
        for validator in validators:
            validator(value)

        return value


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        pattern = re.compile('^[\\w]{3,}')
        if re.match(pattern=pattern, string=value) is None:
            raise serializers.ValidationError('Имя запрещено!')

        if value == 'me':
            raise serializers.ValidationError('Имя "me" запрещено!')
        return value

        # Применяем все валидаторы к значению поля username
    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)

        if User.objects.filter(email=email, username=username).exists():
            return data

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'email занят.'
            )
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'username занят.'
            )
        return data


class VerificationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=250)
