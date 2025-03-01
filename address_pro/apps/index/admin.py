from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.hashers import make_password

admin.site.site_header = 'manage backend'  # 设置header
admin.site.site_title = 'manage backend'  # 设置title


@admin.register(AddressUser)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'name', 'avatar_data', 'juese', 'caozuo',)

    def caozuo(self, obj):
        edit_url = reverse('admin:index_addressuser_change', args=[obj.pk])
        delete_url = reverse('admin:index_addressuser_delete', args=[obj.pk])
        return format_html(

            f'<a href="{edit_url}" style="color: red;">edit</a> | <a href="{delete_url}" style="color: red;">delete</a>'

        )

    caozuo.short_description = u'operation'


@admin.register(BaseSettings)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ('media_url', 'img_data', 'gaode_key', 'caozuo',)

    def caozuo(self, obj):
        edit_url = reverse('admin:index_basesettings_change', args=[obj.pk])
        delete_url = reverse('admin:index_basesettings_delete', args=[obj.pk])
        return format_html(

            f'<a href="{edit_url}" style="color: red;">edit</a> | <a href="{delete_url}" style="color: red;">delete</a>'

        )

    caozuo.short_description = u'operation'


@admin.register(Order)
class FlowerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'shunxu', 'user', 'desc', 'level', 'date', 'is_valid', 'state', 
        'start_time', 'end_time', 'start_address', 'end_address', 
        'connect_user', 'connect_phone', 'price', 'get_services', 'caozuo',
    )

    def get_services(self, obj):
        services = OrderService.objects.filter(order=obj)
        return ", ".join([f"{s.service.category} ({s.service.price})" for s in services])
    
    get_services.short_description = 'Services'

    def caozuo(self, obj):
        edit_url = reverse('admin:index_order_change', args=[obj.pk])
        delete_url = reverse('admin:index_order_delete', args=[obj.pk])
        return format_html(
            f'<a href="{edit_url}" style="color: red;">edit</a> | <a href="{delete_url}" style="color: red;">delete</a>'
        )

    caozuo.short_description = u'operation'


@admin.register(OrderType)
class FlowerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'caozuo',)

    def caozuo(self, obj):
        edit_url = reverse('admin:index_ordertype_change', args=[obj.pk])
        delete_url = reverse('admin:index_ordertype_delete', args=[obj.pk])
        return format_html(

            f'<a href="{edit_url}" style="color: red;">edit</a> | <a href="{delete_url}" style="color: red;">delete</a>'

        )

    caozuo.short_description = u'operation'


@admin.register(ServiceType)
class FlowerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'caozuo',)

    def caozuo(self, obj):
        edit_url = reverse('admin:index_servicetype_change', args=[obj.pk])
        delete_url = reverse('admin:index_servicetype_delete', args=[obj.pk])
        return format_html(

            f'<a href="{edit_url}" style="color: red;">edit</a> | <a href="{delete_url}" style="color: red;">delete</a>'

        )

    caozuo.short_description = u'operation'


@admin.register(Address)
class FlowerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'caozuo',)

    def caozuo(self, obj):
        edit_url = reverse('admin:index_address_change', args=[obj.pk])
        delete_url = reverse('admin:index_address_delete', args=[obj.pk])
        return format_html(

            f'<a href="{edit_url}" style="color: red;">edit</a> | <a href="{delete_url}" style="color: red;">delete</a>'

        )

    caozuo.short_description = u'operation'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'service_type', 'address', 'price']
    search_fields = ['category']


@admin.register(OrderService)
class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'service']
    search_fields = ['order__desc', 'service__category']
