from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from djoser.serializers import UserDeleteSerializer, CurrentPasswordSerializer
from rest_framework import exceptions, serializers
from rest_framework.exceptions import ValidationError

from djoser import utils
from djoser.compat import get_user_email, get_user_email_field_name
from djoser.conf import settings

User = get_user_model()


# class CustomUserSerializer(UserSerializer):
#     class Meta:
#         model = CustomUser
#         fields = '__all__'

class CustomAdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)


class CustomAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'name', 'phone', 'birth_date',)


class CustomUserDeleteSerializer(
    CurrentPasswordSerializer,  # Users have to send password to delete his own account
    serializers.ModelSerializer
):
    class Meta:
        model = User
        fields = ('password', 'is_active',)
