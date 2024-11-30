from rest_framework import serializers
from .models import AddressUser, BaseSettings, Order


class GetLoginImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseSettings
        fields = ['img', ]


class GetJueSeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressUser
        fields = ['juese', ]


class GetUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressUser
        fields = ['name', 'avatar', ]


class GetAllOrderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id','user_name', 'desc', 'level', 'date', 'is_valid', 'state', 'start_time', 'end_time', 'start_address',
                  'end_address', 'start_location', 'end_location', 'uuid']


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressUser
        fields = ['name', 'id']


class GetOneOrderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id','user_name', 'desc', 'level', 'date', 'is_valid', 'state', 'start_time', 'end_time', 'start_address',
                  'end_address', 'start_location', 'end_location', 'uuid']