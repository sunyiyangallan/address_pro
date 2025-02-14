from django.db import models
from address_pro.utils.models import BaseModel
from django.utils.html import format_html
from django.contrib.auth.models import AbstractUser
import uuid as get_uuid


def get_media_url():
    media_url = BaseSettings.objects.all().first().media_url
    return media_url


# 用户表
class AddressUser(BaseModel):
    uuid = models.UUIDField(verbose_name='uuid', default=get_uuid.uuid4)
    avatar = models.FileField(upload_to='avatar', verbose_name='avatar', null=True, blank=True, default='avatar/avatar.svg')
    name = models.CharField(max_length=64, verbose_name='username', null=True, blank=True)
    password = models.CharField(max_length=128, verbose_name='password', null=True, blank=True)
    juese = models.SmallIntegerField(choices=((0, 'Driver'), (1, 'Dispatcher'), (2, 'Admin')), verbose_name='role', default=0)
    token = models.CharField(verbose_name='Token', max_length=128, null=True, blank=True)

    def avatar_data(self):
        return format_html(
            f'<img src="{get_media_url()}{self.avatar}" width="70px", height="70px"/>',

        )

    avatar_data.short_description = u'avatar'

    def __str__(self):
        juese_text = ''
        if self.juese == 0:
            juese_text = 'Driver'
        if self.juese == 1:
            juese_text = 'Dispatcher'
        if self.juese == 2:
            juese_text = 'Admin'
        return f'{juese_text} {self.name}'


# 基础设置表
class BaseSettings(BaseModel):
    media_url = models.CharField(verbose_name='media_url', max_length=64, null=True, blank=True)
    img = models.FileField(upload_to='avatar', verbose_name='backend_img', null=True, blank=True)
    gaode_key = models.CharField(verbose_name='gaode_key', max_length=128, null=True, blank=True)
    code = models.CharField(verbose_name='auth_code', max_length=64, null=True, blank=True)

    class Meta:
        db_table = 'base_settings'
        verbose_name = 'basetings'
        verbose_name_plural = verbose_name

    def img_data(self):
        return format_html(
            f'<img src="{get_media_url()}{self.img}" width="100px", height="70px"/>',

        )

    img_data.short_description = u'login_backend_img'


class Order(BaseModel):
    uuid = models.UUIDField(verbose_name='uuid', default=get_uuid.uuid4)
    user = models.ForeignKey(to='AddressUser', verbose_name='user', null=True, blank=True, on_delete=models.CASCADE)
    desc = models.CharField(verbose_name='desc', max_length=125, null=True, blank=True)
    level = models.SmallIntegerField(choices=((0, 'Low'), (1, 'Mid'), (2, 'High')), verbose_name='priority', default=0)
    date = models.DateTimeField(verbose_name='date', null=True, blank=True)
    is_valid = models.BooleanField(verbose_name='is_valid', default=True)
    state = models.SmallIntegerField(choices=((-1, 'unallocated'), (0, 'unstarted'), (1, 'ongoings'), (2, 'completed')), verbose_name='state',
                                     default=-1)
    start_time = models.DateTimeField(verbose_name='start_time', null=True, blank=True)
    end_time = models.DateTimeField(verbose_name='end_time', null=True, blank=True)
    start_address = models.CharField(verbose_name='start_address', max_length=125, null=True, blank=True)
    end_address = models.CharField(verbose_name='end_address', max_length=125, null=True, blank=True)
    start_location = models.CharField(verbose_name='start_location', max_length=125, null=True, blank=True)
    end_location = models.CharField(verbose_name='end_location', max_length=125, null=True, blank=True)
    num = models.IntegerField(verbose_name='num', default=0, null=True, blank=True)
    shunxu = models.IntegerField(verbose_name='order', null=True, blank=True)
    connect_user = models.CharField(verbose_name='connect_user', max_length=64, null=True, blank=True)
    connect_phone = models.CharField(verbose_name='connect_phone', max_length=64, null=True, blank=True)
    type = models.ManyToManyField(to='OrderType', verbose_name='type', null=True, blank=True)
    price = models.FloatField(verbose_name='price', default=0)
    is_reback = models.BooleanField(verbose_name='is_reback', default=False)
    update_order = models.OneToOneField(to='UpdateOrder', on_delete=models.CASCADE, null=True, blank=True, )
    type_str = models.TextField(verbose_name='type_str', null=True, blank=True)

    service_list = models.ManyToManyField(to='Service', verbose_name='service_list', null=True, blank=True)
    remark = models.TextField(verbose_name='remark', null=True, blank=True)

class OrderType(BaseModel):
    name = models.CharField(verbose_name='name', max_length=64, null=True, blank=True)
    price = models.FloatField(verbose_name='price', default=0)

    def __str__(self):
        return self.name


class UpdateOrder(BaseModel):
    desc = models.CharField(verbose_name='desc', max_length=125, null=True, blank=True)

    level = models.SmallIntegerField(choices=((0, 'Low'), (1, 'Mid'), (2, 'High')), verbose_name='priority', default=0)
    date = models.DateTimeField(verbose_name='date', null=True, blank=True)
    end_address = models.CharField(verbose_name='end_address', max_length=125, null=True, blank=True)
    num = models.IntegerField(verbose_name='num', default=0, null=True, blank=True)
    connect_user = models.CharField(verbose_name='connect_user', max_length=64, null=True, blank=True)
    connect_phone = models.CharField(verbose_name='connect_phone', max_length=64, null=True, blank=True)
    type = models.ManyToManyField(to='OrderType', verbose_name='type', null=True, blank=True)
    price = models.FloatField(verbose_name='price', default=0)
    type_str = models.TextField(verbose_name='type_str', null=True, blank=True)
    service_list = models.ManyToManyField(to='Service', verbose_name='service_list', null=True, blank=True)
    remark = models.TextField(verbose_name='remark', null=True, blank=True)


class ServiceType(BaseModel):
    name = models.CharField(verbose_name='name', max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name


class Address(BaseModel):
    name = models.CharField(verbose_name='name', max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name


class Service(BaseModel):
    address = models.ForeignKey(to='Address', verbose_name='address', null=True, blank=True, on_delete=models.CASCADE)
    service_type = models.ForeignKey(to='ServiceType', verbose_name='service_type', null=True, blank=True, on_delete=models.CASCADE)
    category = models.CharField(verbose_name='category', max_length=128, null=True, blank=True)
    price = models.FloatField(verbose_name='price', null=True, blank=True)



