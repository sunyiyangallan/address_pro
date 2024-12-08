from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.hashers import make_password

admin.site.site_header = '管理后台'  # 设置header
admin.site.site_title = '管理后台'  # 设置title


@admin.register(AddressUser)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'avatar_data', 'juese', 'caozuo',)

    def caozuo(self, obj):
        edit_url = reverse('admin:index_addressuser_change', args=[obj.pk])
        delete_url = reverse('admin:index_addressuser_delete', args=[obj.pk])
        return format_html(

            f'<a href="{edit_url}" style="color: red;">编辑</a> | <a href="{delete_url}" style="color: red;">删除</a>'

        )

    caozuo.short_description = u'操作'


@admin.register(BaseSettings)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('media_url', 'img_data', 'gaode_key', 'caozuo',)

    def caozuo(self, obj):
        edit_url = reverse('admin:index_basesettings_change', args=[obj.pk])
        delete_url = reverse('admin:index_basesettings_delete', args=[obj.pk])
        return format_html(

            f'<a href="{edit_url}" style="color: red;">编辑</a> | <a href="{delete_url}" style="color: red;">删除</a>'

        )

    caozuo.short_description = u'操作'


@admin.register(Order)
class FlowerAdmin(admin.ModelAdmin):
    list_display = (
        'shunxu', 'type', 'user', 'desc', 'level', 'date', 'is_valid', 'state', 'start_time', 'end_time', 'start_address',
        'end_address', 'connect_user', 'connect_phone', 'caozuo',)

    def caozuo(self, obj):
        edit_url = reverse('admin:index_order_change', args=[obj.pk])
        delete_url = reverse('admin:index_order_delete', args=[obj.pk])
        return format_html(

            f'<a href="{edit_url}" style="color: red;">编辑</a> | <a href="{delete_url}" style="color: red;">删除</a>'

        )

    caozuo.short_description = u'操作'


@admin.register(OrderType)
class FlowerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'caozuo',)

    def caozuo(self, obj):
        edit_url = reverse('admin:index_ordertype_change', args=[obj.pk])
        delete_url = reverse('admin:index_ordertype_delete', args=[obj.pk])
        return format_html(

            f'<a href="{edit_url}" style="color: red;">编辑</a> | <a href="{delete_url}" style="color: red;">删除</a>'

        )

    caozuo.short_description = u'操作'
