from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.hashers import make_password

admin.site.site_header = '管理后台'  # 设置header
admin.site.site_title = '管理后台'  # 设置title


@admin.register(AddressUser)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'avatar_data', 'caozuo',)

    def caozuo(self, obj):
        edit_url = reverse('admin:index_addressuser_change', args=[obj.pk])
        delete_url = reverse('admin:index_addressuser_delete', args=[obj.pk])
        return format_html(

            f'<a href="{edit_url}" style="color: red;">编辑</a> | <a href="{delete_url}" style="color: red;">删除</a>'

        )

    caozuo.short_description = u'操作'


@admin.register(BaseSettings)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('media_url', 'caozuo',)

    def caozuo(self, obj):
        edit_url = reverse('admin:index_basesettings_change', args=[obj.pk])
        delete_url = reverse('admin:index_basesettings_delete', args=[obj.pk])
        return format_html(

            f'<a href="{edit_url}" style="color: red;">编辑</a> | <a href="{delete_url}" style="color: red;">删除</a>'

        )

    caozuo.short_description = u'操作'