from django.db import models
from address_pro.utils.models import BaseModel
from django.utils.html import format_html
from django.contrib.auth.models import AbstractUser
import uuid as get_uuid


def get_media_url():
    media_url = BaseSettings.objects.all().first().media_url
    return media_url


class AddressUser(BaseModel):
    uuid = models.UUIDField(verbose_name='用户唯一标识', default=get_uuid.uuid4)
    avatar = models.FileField(upload_to='avatar', verbose_name='头像', null=True, blank=True)

    def avatar_data(self):
        return format_html(
            f'<img src="{get_media_url()}{self.avatar}" width="70px", height="70px"/>',

        )

    avatar_data.short_description = u'头像'


# 基础设置表
class BaseSettings(BaseModel):
    media_url = models.CharField(verbose_name='media_url', max_length=64, null=True, blank=True)

    class Meta:
        db_table = 'base_settings'
        verbose_name = '基础设置表'
        verbose_name_plural = verbose_name
