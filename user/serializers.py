from rest_framework import serializers
from .models import User, PasswordRecovery


class UserSerializer(serializers.ModelSerializer):
    # date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'full_name', 'bonuses', 'password')
        extra_kwargs = {'password': {'write_only': True},
                        'email': {'required': False},
                        'phone': {'required': False},
                        }

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordRecoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordRecovery
        fields = ('user', 'link')
