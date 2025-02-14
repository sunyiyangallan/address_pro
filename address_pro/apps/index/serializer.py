from rest_framework import serializers
from .models import AddressUser, BaseSettings, Order, OrderType, UpdateOrder,ServiceType,Address,Service


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



class ServiceSerializer(serializers.ModelSerializer):
    address_name = serializers.CharField(source='address.name', read_only=True)
    service_type_name = serializers.CharField(source='service_type.name', read_only=True)
    class Meta:
        model = Service
        fields = ['id', 'address_name', 'service_type_name', 'category', 'price']


class GetAllOrderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    type_name = serializers.CharField(source='type_str', read_only=True)
    service_list = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_name', 'desc', 'level', 'date', 'is_valid', 'state', 'start_time', 'end_time',
                  'start_address',
                  'end_address', 'start_location', 'end_location', 'uuid', 'num', 'shunxu', 'connect_user',
                  'connect_phone', 'type_name', 'price', 'is_reback', 'update_order', 'service_list', 'remark']


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressUser
        fields = ['name', 'id']


class GetOneOrderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    type_name = serializers.CharField(source='type_str', read_only=True)
    service_list = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_name', 'desc', 'level', 'date', 'is_valid', 'state', 'start_time', 'end_time',
                  'start_address',
                  'end_address', 'start_location', 'end_location', 'uuid','num', 'shunxu', 'connect_user', 'connect_phone',
                  'type_name', 'price', 'is_reback', 'remark','service_list' ]


class GetOrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = ['name', 'price', 'id']



class GetUpdateOrderSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='type_str', read_only=True)
    service_list = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = UpdateOrder
        fields = ['desc', 'level', 'date',
                  'end_address', 'connect_user', 'connect_phone', 'price', 'num', 'id', 'type_name', 'service_list','remark']


class GetAllServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['id', 'name']


class GetAllAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'name']


class GetServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'address', 'service_type', 'category', 'price']


