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
    uuid = models.UUIDField(verbose_name='用户唯一标识', default=get_uuid.uuid4)
    avatar = models.FileField(upload_to='avatar', verbose_name='头像', null=True, blank=True, default='avatar/avatar.svg')
    name = models.CharField(max_length=64, verbose_name='用户名', null=True, blank=True)
    password = models.CharField(max_length=128, verbose_name='密码', null=True, blank=True)
    juese = models.SmallIntegerField(choices=((0, '普通员工'), (1, '高级员工'), (2, '管理员')), verbose_name='角色', default=0)
    token = models.CharField(verbose_name='Token', max_length=128, null=True, blank=True)

    def avatar_data(self):
        return format_html(
            f'<img src="{get_media_url()}{self.avatar}" width="70px", height="70px"/>',

        )

    avatar_data.short_description = u'头像'


    def __str__(self):
        juese_text = ''
        if self.juese == 0:
            juese_text = '普通员工'
        if self.juese == 1:
            juese_text = '高级员工'
        if self.juese == 2:
            juese_text = '管理员'
        return f'{juese_text} {self.name}'


# 基础设置表
class BaseSettings(BaseModel):
    media_url = models.CharField(verbose_name='media_url', max_length=64, null=True, blank=True)
    img = models.FileField(upload_to='avatar', verbose_name='注册登录背景图', null=True, blank=True)
    gaode_key = models.CharField(verbose_name='高德key', max_length=128, null=True, blank=True)
    code = models.CharField(verbose_name='授权码', max_length=64, null=True,blank=True)


    class Meta:
        db_table = 'base_settings'
        verbose_name = '基础设置表'
        verbose_name_plural = verbose_name

    def img_data(self):
        return format_html(
            f'<img src="{get_media_url()}{self.img}" width="100px", height="70px"/>',

        )

    img_data.short_description = u'注册登录背景图'


class Order(BaseModel):
    uuid = models.UUIDField(verbose_name='订单唯一标识', default=get_uuid.uuid4)
    user = models.ForeignKey(to='AddressUser', verbose_name='员工', null=True, blank=True, on_delete=models.CASCADE)
    desc = models.CharField(verbose_name='描述', max_length=125, null=True, blank=True)
    level = models.SmallIntegerField(choices=((0, '普通'), (1, '加急'), (2, '紧急')), verbose_name='优先级', default=0)
    date = models.DateTimeField(verbose_name='截至日期', null=True, blank=True)
    is_valid = models.BooleanField(verbose_name='是否有效', default=True)
    state = models.SmallIntegerField(choices=((0, '未开始'), (1, '进行中'), (2, '已完成')), verbose_name='状态', default=0)
    start_time = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_time = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)
    start_address = models.CharField(verbose_name='起始地', max_length=125, null=True, blank=True)
    end_address = models.CharField(verbose_name='目的地', max_length=125, null=True, blank=True)
    start_location = models.CharField(verbose_name='起始地经纬度', max_length=125, null=True, blank=True)
    end_location = models.CharField(verbose_name='目的地经纬度', max_length=125, null=True, blank=True)
    num = models.IntegerField(verbose_name='派送数量', default=0, null=True,blank=True)
    shunxu = models.IntegerField(verbose_name='顺序', null=True, blank=True)








