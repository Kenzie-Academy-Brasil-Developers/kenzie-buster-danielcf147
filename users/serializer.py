from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password
from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(
        max_length=127,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="email already registered."
            )
        ],
    )
    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="username already taken."
            )
        ],
    )
    password = password = serializers.CharField(max_length=127, write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField(allow_null=True, required=False)
    is_employee = serializers.BooleanField(allow_null=True, default=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data: dict) -> User:
        if validated_data["is_employee"] == True:
            validated_data["is_superuser"] = True
            validated_data["is_staff"] = True

        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict):

        if validated_data["password"]:
            validated_data["password"] = make_password(validated_data["password"])

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=150, write_only=True)
#     password = password = serializers.CharField(max_length=127, write_only=True)
