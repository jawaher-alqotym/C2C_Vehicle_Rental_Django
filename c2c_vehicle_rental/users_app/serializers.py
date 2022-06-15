from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User



class UserCredentialSerializer(serializers.ModelSerializer):
    driver_licence = serializers.SerializerMethodField(required=False)

    class Meta:
        model = UserCredential
        fields = '__all__'

    def get_driver_licence(self, record: UserCredential):
        return record.driver_licence.url


class UserSerializer(serializers.ModelSerializer):
    user_credential = UserCredentialSerializer()

    class Meta:
        model = User
        fields = ['username','email','first_name','last_name', 'password', 'user_credential']

    def create(self, validated_data):
        user_credential = validated_data.pop('user_credential')
        user_instance = User.objects.create(**validated_data)

        UserCredential.objects.create(user=user_instance,phone_number= user_credential['phone_number'])
        return user_instance
