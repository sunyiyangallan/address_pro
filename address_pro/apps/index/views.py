from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from utils.response import ApiResponse
from address_pro.utils.md5 import md5_encrypt
from .models import AddressUser, BaseSettings, Order, OrderType, UpdateOrder, ServiceType, Address, Service
from .serializer import GetLoginImgSerializer, GetJueSeSerializer, GetUserInfoSerializer, GetAllOrderSerializer, \
    GetUserSerializer, GetOneOrderSerializer, GetOrderTypeSerializer, GetUpdateOrderSerializer, \
    GetAllServiceTypeSerializer, GetAllAddressSerializer, ServiceSerializer
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import ExtractWeekDay
from rest_framework.filters import SearchFilter
import requests
import json
from datetime import datetime
from django.db.models import Case, When


# 获取背景图
class GetLoginImgView(GenericViewSet, ListModelMixin):
    queryset = BaseSettings.objects.all()
    serializer_class = GetLoginImgSerializer


# 注册
class RegisterView(APIView):
    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        juese = request.data.get('juese')
        code = request.data.get('code')
        token = md5_encrypt(f'{name}{juese}{password}')
        setting_obj = BaseSettings.objects.all().first()

        return_data = {
            'token': token
        }
        user_obj = AddressUser.objects.filter(juese=int(juese), name=name).first()
        if user_obj:
            return ApiResponse(code=333, msg="用户已经存在")

        else:
            if int(juese) == 2:
                if code:
                    if setting_obj.code != code:
                        return ApiResponse(code=444, msg="没有权限")
                    else:
                        AddressUser.objects.create(name=name, password=password, juese=int(juese), token=token)
                        return ApiResponse(data=return_data)
                else:
                    return ApiResponse(code=444, msg="注册失败")
            else:
                AddressUser.objects.create(name=name, password=password, juese=int(juese), token=token)
                return ApiResponse(data=return_data)


# 登录
class LoginView(APIView):
    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        juese = request.data.get('juese')
        token = md5_encrypt(f'{name}{juese}{password}')

        return_data = {
            'token': token
        }
        user_obj = AddressUser.objects.filter(juese=int(juese), name=name).first()
        if user_obj:
            if token != user_obj.token:
                return ApiResponse(code=444, msg='密码错误')
            else:

                return ApiResponse(data=return_data, msg='登录成功')
        else:
            return ApiResponse(code=555, msg='没有此用户, 请先注册')


# 判断角色类型
class JueSeView(GenericViewSet, ListModelMixin):
    queryset = AddressUser.objects.all()
    serializer_class = GetJueSeSerializer

    filter_backends = [SearchFilter]
    search_fields = ['token', ]


# 获取用户信息
class GetUserInfoView(GenericViewSet, ListModelMixin):
    queryset = AddressUser.objects.all()
    serializer_class = GetUserInfoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['token', ]


class GetAllOrderView(GenericViewSet, ListModelMixin):
    # queryset = Order.objects.all().order_by('state', 'id')
    serializer_class = GetAllOrderSerializer
    filter_backends = [SearchFilter]
    search_fields = ['desc', 'shunxu', ]

    def get_queryset(self):
        # 定义状态的排序顺序
        state_order = Case(
            When(state=1, then=0),
            When(state=0, then=1),
            When(state=2, then=2),
        )

        # 获取基础查询集并应用排序和过滤
        queryset = Order.objects.all().annotate(state_order=state_order).order_by('state_order', 'shunxu')

        # 筛选 user 字段未赋值的订单
        # queryset = queryset.filter(user__isnull=False)
        return queryset


class GetUserOrderView(GenericViewSet, ListModelMixin):
    queryset = Order.objects.filter(state__in=[1, 0]).order_by('shunxu')
    serializer_class = GetAllOrderSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__token', 'desc', 'shunxu', ]

    # def get_queryset(self):
    #     # 定义状态的排序顺序
    #     state_order = Case(
    #         When(state=1, then=0),
    #         When(state=0, then=1),
    #         When(state=2, then=2),
    #     )
    #
    #     # 获取基础查询集并应用排序和过滤
    #     queryset = Order.objects.all().annotate(state_order=state_order).order_by('shunxu', 'id')
    #     return queryset


class SearchAddressView(APIView):
    def post(self, request):

        setting_obj = BaseSettings.objects.all().first()

        name = request.data.get('name')

        response = requests.post(
            url=f'https://restapi.amap.com/v5/place/text?keywords={name}&key={setting_obj.gaode_key}')
        response_dic = json.loads(response.content)
        if response_dic.get('status') == '1':
            return_data = response_dic.get('pois')
            return ApiResponse(data=return_data)
        else:

            return ApiResponse(code=333)


# 每日新增订单量
class GetDayAddOrderView(APIView):
    def get(self, request):

        # 获取当前时间
        now = timezone.now()

        # 计算过去7天的开始日期
        start_date = now - timedelta(days=6)

        # 查询过去7天的数据
        data = Order.objects.filter(created_time__gte=start_date, created_time__lte=now)

        # 按星期几分组并统计数量
        weekly_data = data.annotate(weekday=ExtractWeekDay('created_time')).values('weekday').annotate(
            count=Count('id')).order_by('weekday')

        # 将结果转换为字典格式，方便前端使用
        result = {
            'Monday': 0,
            'Tuesday': 0,
            'Wednesday': 0,
            'Thursday': 0,
            'Friday': 0,
            'Saturday': 0,
            'Sunday': 0
        }

        for entry in weekly_data:
            weekday = entry['weekday']
            count = entry['count']

            if weekday == 1:
                result['Monday'] = count
            elif weekday == 2:
                result['Tuesday'] = count
            elif weekday == 3:
                result['Wednesday'] = count
            elif weekday == 4:
                result['Thursday'] = count
            elif weekday == 5:
                result['Friday'] = count
            elif weekday == 6:
                result['Saturday'] = count
            elif weekday == 7:
                result['Sunday'] = count
            # 获取今天是星期几
        today_weekday = now.isoweekday()

        # 重新排序结果字典，使其从今天的星期几开始
        sorted_result = {}
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        start_index = (today_weekday - 1) % 7
        for i in range(7):
            day = days_of_week[(start_index + i) % 7]
            sorted_result[day[:3]] = result[day]  # 截取前三个字母
        days_list = list(sorted_result.keys())
        counts_list = list(sorted_result.values())
        today_day = days_list.pop(0)
        today_count = counts_list.pop(0)
        days_list.append(today_day)
        counts_list.append(today_count)

        return ApiResponse(data={'days_list': days_list, 'counts_list': counts_list})


# 每日订单的完成量
class GetDayCompleteOrderView(APIView):
    def get(self, request):

        # 获取当前时间
        now = timezone.now()

        # 计算过去7天的开始日期
        start_date = now - timedelta(days=6)

        # 查询过去7天的数据
        data = Order.objects.filter(end_time__gte=start_date, end_time__lte=now)

        # 按星期几分组并统计数量
        weekly_data = data.annotate(weekday=ExtractWeekDay('end_time')).values('weekday').annotate(
            count=Count('id')).order_by('weekday')

        # 将结果转换为字典格式，方便前端使用
        result = {
            'Monday': 0,
            'Tuesday': 0,
            'Wednesday': 0,
            'Thursday': 0,
            'Friday': 0,
            'Saturday': 0,
            'Sunday': 0
        }

        for entry in weekly_data:
            weekday = entry['weekday']
            count = entry['count']

            if weekday == 1:
                result['Monday'] = count
            elif weekday == 2:
                result['Tuesday'] = count
            elif weekday == 3:
                result['Wednesday'] = count
            elif weekday == 4:
                result['Thursday'] = count
            elif weekday == 5:
                result['Friday'] = count
            elif weekday == 6:
                result['Saturday'] = count
            elif weekday == 7:
                result['Sunday'] = count
            # 获取今天是星期几
        today_weekday = now.isoweekday()

        # 重新排序结果字典，使其从今天的星期几开始
        sorted_result = {}
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        start_index = (today_weekday - 1) % 7
        for i in range(7):
            day = days_of_week[(start_index + i) % 7]
            sorted_result[day[:3]] = result[day]  # 截取前三个字母
        days_list = list(sorted_result.keys())
        counts_list = list(sorted_result.values())
        today_day = days_list.pop(0)
        today_count = counts_list.pop(0)
        days_list.append(today_day)
        counts_list.append(today_count)

        return ApiResponse(data={'days_list': days_list, 'counts_list': counts_list})


# 获取人员角色分布数据
class GetJueSeView(APIView):
    def get(self, request):
        count1 = AddressUser.objects.filter(juese=0).count()
        count2 = AddressUser.objects.filter(juese=1).count()
        count3 = AddressUser.objects.filter(juese=2).count()

        data = [
            {'value': count3, 'name': 'Admin'},
            {'value': count1, 'name': 'Driver'},
            {'value': count2, 'name': 'Dispatcher'},
        ]

        return ApiResponse(data=data)


# 获取总订单状态数据
class GetOrderStateView(APIView):
    def get(self, request):
        count1 = Order.objects.filter(state=0).count()
        count2 = Order.objects.filter(state=1).count()
        count3 = Order.objects.filter(state=2).count()

        data = [
            {'value': count1, 'name': 'unstarted orders'},
            {'value': count2, 'name': 'Ongoing Orders'},
            {'value': count3, 'name': 'Completed Orders'},
        ]

        return ApiResponse(data=data)


# 获取所有的送货员
class GetAllCommonUserView(GenericViewSet, ListModelMixin):
    queryset = AddressUser.objects.filter(juese=0).all()
    serializer_class = GetUserSerializer


# 创建订单
class CreateOrderView(APIView):
    def post(self, request):
        desc = request.data.get('desc', '')
        level = int(request.data.get('level'))
        # date = datetime.strptime(request.data.get('time3'), '%Y-%m-%dT%H:%M:%S.%fZ')
        date = request.data.get('time3')
        end_address = request.data.get('search_end')
        # type_dic = request.data.get('search_num')
        price = request.data.get('price')
        service_list = request.data.get('service_list')
        connect_user = request.data.get('connect_user')
        connect_phone = request.data.get('connect_phone')
        remark = request.data.get('remark')

        text_str = ''

        service_id_list = []
        for i in service_list:
            service_id_list.append(i.get('id'))

        service_obj = Service.objects.filter(id__in=service_id_list).all()

        Order.objects.create(desc=desc, level=level, date=date,end_address=end_address,remark=remark,
                             price=price, connect_user=connect_user, connect_phone=connect_phone)

        order_obj = Order.objects.all().order_by('-id').first()
        if service_obj:
            for i in service_obj:
                order_obj.service_list.add(i)

        # type_obj_list = OrderType.objects.all().order_by('id')
        type_id_list = []
        # for key, values in type_dic.items():
        #     if values == 0:
        #         continue
        #     type_id_list.append(type_obj_list[int(key)].id)
        #     new_type_obj = OrderType.objects.filter(id=type_obj_list[int(key)].id).first()
        #     text_str += f'类型:{new_type_obj.name},数量:{values}; '
        #
        # type_obj = OrderType.objects.filter(id__in=type_id_list).all()
        # Order.objects.create(desc=desc, level=level, date=date, end_address=end_address,
        #                      price=price, connect_user=connect_user, connect_phone=connect_phone, type_str=text_str)
        # order_obj = Order.objects.all().order_by('-id').first()
        # if type_obj:
        #     for i in type_obj:
        #         order_obj.type.add(i)

        return ApiResponse()


class GetOneOrderView(GenericViewSet, ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = GetOneOrderSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', ]


class StartOrderView(APIView):
    def get(self, request):
        id = request.query_params.get('id')
        Order.objects.filter(id=id).update(state=1, start_time=datetime.now())
        return ApiResponse()


class EndOrderView(APIView):
    def get(self, request):
        id = request.query_params.get('id')
        Order.objects.filter(id=id).update(state=2, end_time=datetime.now())
        return ApiResponse()


class NullOrderView(GenericViewSet, ListModelMixin):
    queryset = Order.objects.filter(user__isnull=True).all()
    serializer_class = GetAllOrderSerializer


# 更新订单
class UpdateOrderView(APIView):
    def post(self, request):
        user = request.data.get('user')
        order = request.data.get('order')
        shunxu = int(request.data.get('num'))

        user_obj = AddressUser.objects.filter(id=user).first()
        Order.objects.filter(id=order).update(user=user_obj, shunxu=shunxu, state=0)

        return ApiResponse()


# 获取订单类型
class GetOrderTypeView(GenericViewSet, ListModelMixin):
    queryset = OrderType.objects.all().order_by('id')
    serializer_class = GetOrderTypeSerializer


# 获取当前最大顺序
class GetMaxView(APIView):
    def get(self, request):

        id = request.query_params.get('uid')
        order_obj = Order.objects.filter(shunxu__isnull=False, user__id=int(id)).order_by('-shunxu').first()

        if order_obj:
            max_num = order_obj.shunxu + 1
            return ApiResponse(data={'max': max_num})
        else:
            return ApiResponse(data={'max': 1})


# 修改订单
class PaiUpdateOrderView(APIView):
    def post(self, request):

        juese = request.data.get('juese')

        order_id = request.data.get('order_id')
        desc = request.data.get('desc')
        remark = request.data.get('remark')

        try:
            level = int(request.data.get('level'))
        except:
            if request.data.get('level') == 'Low':
                level = 0
            elif request.data.get('level') == 'Mid':
                level = 1
            else:
                level = 2

        try:
            date = request.data.get('time3')

        except:
            date = datetime.strptime(request.data.get('time3'), '%Y-%m-%dT%H:%M:%S.%fZ')

        end_address = request.data.get('search_end')
        # type_dic = request.data.get('search_num')
        service_list = request.data.get('service_list')
        price = request.data.get('price')
        connect_user = request.data.get('connect_user')
        connect_phone = request.data.get('connect_phone')
        text_str = ''

        # type_obj_list = OrderType.objects.all().order_by('id')

        service_id_list = []
        for i in service_list:
            service_id_list.append(i.get('id'))

        service_obj = Service.objects.filter(id__in=service_id_list).all()

        if service_obj:
            if juese == 0:
                UpdateOrder.objects.create(desc=desc, level=level, date=date,end_address=end_address,remark=remark,
                                                   connect_user=connect_user, connect_phone=connect_phone,
                                                   price=price)
                UpdateOrder_obj = UpdateOrder.objects.all().order_by('-id').first()
                for i in service_obj:
                    UpdateOrder_obj.service_list.add(i)
                Order.objects.filter(id=order_id).update(update_order=UpdateOrder_obj)
                return ApiResponse()
                # UpdateOrder.objects.create(desc=desc, level=level, date=date, end_address=end_address,
                #                            connect_user=connect_user, connect_phone=connect_phone, type_str=text_str,
                #                            price=price)
                # UpdateOrder_obj = UpdateOrder.objects.all().order_by('-id').first()
                # for i in type_obj:
                #     UpdateOrder_obj.type.add(i)
                # Order.objects.filter(id=order_id).update(update_order=UpdateOrder_obj)
                # return ApiResponse()
            else:
                order_obj = Order.objects.filter(id=order_id).first()
                if order_obj.service_list:
                    order_obj.service_list.clear()
                for i in service_obj:
                    order_obj.service_list.add(i)
                Order.objects.filter(id=order_id).update(desc=desc, level=level, date=date,end_address=end_address,remark=remark,
                                                         connect_user=connect_user, connect_phone=connect_phone,
                                                          price=price)
                return ApiResponse()




        # Order.objects.create(desc=desc, level=level, date=date,
        #                      price=price, connect_user=connect_user, connect_phone=connect_phone)
        #
        # order_obj = Order.objects.all().order_by('-id').first()
        # if service_obj:
        #     for i in service_obj:
        #         order_obj.service_list.add(i)


        type_id_list = []
        # for key, values in type_dic.items():
        #     if values == 0:
        #         continue
        #     type_id_list.append(type_obj_list[int(key)].id)
        #     new_type_obj = OrderType.objects.filter(id=type_obj_list[int(key)].id).first()
        #     text_str += f'类型:{new_type_obj.name},数量:{values}; '
        #
        # type_obj = OrderType.objects.filter(id__in=type_id_list).all()

        # if type_obj:
        #
        #     if juese == 0:
        #
        #         UpdateOrder.objects.create(desc=desc, level=level, date=date, end_address=end_address,
        #                                    connect_user=connect_user, connect_phone=connect_phone, type_str=text_str,
        #                                    price=price)
        #         UpdateOrder_obj = UpdateOrder.objects.all().order_by('-id').first()
        #         for i in type_obj:
        #             UpdateOrder_obj.type.add(i)
        #         Order.objects.filter(id=order_id).update(update_order=UpdateOrder_obj)
        #         return ApiResponse()
        #     else:
        #         order_obj = Order.objects.filter(id=order_id).first()
        #         for i in type_obj:
        #             order_obj.type.add(i)
        #         Order.objects.filter(id=order_id).update(desc=desc, level=level, date=date, end_address=end_address,
        #                                                  connect_user=connect_user, connect_phone=connect_phone,
        #                                                  type_str=text_str, price=price)
        #         return ApiResponse()


# 获取修改的订单
class GetUpdateOrderView(GenericViewSet, ListModelMixin):
    # queryset = UpdateOrder.objects.all()
    serializer_class = GetUpdateOrderSerializer

    def get_queryset(self):
        # 获取请求参数中的 id
        order_id = self.request.query_params.get('id', None)
        if order_id:
            return UpdateOrder.objects.filter(id=order_id)
        else:
            return UpdateOrder.objects.all().order_by('-id')




class ConfirmOrderView(APIView):
    def get(self, request):
        order_id = int(request.query_params.get('order_id'))
        update_id = int(request.query_params.get('update_id'))

        update_order = UpdateOrder.objects.filter(id=update_id).first()
        desc = update_order.desc
        level = update_order.level
        date = update_order.date
        end_address = update_order.end_address
        connect_user = update_order.connect_user
        connect_phone = update_order.connect_phone
        remark = update_order.remark
        # type_str = update_order.type_str
        price = update_order.price

        service_id_list = []

        for i in update_order.service_list.all():
            service_id_list.append(i.id)

        order_obj = Order.objects.filter(id=order_id).first()
        order_obj.service_list.clear()

        service_obj = Service.objects.filter(id__in=service_id_list).all()
        if service_obj:
            for k in service_obj:
                order_obj.service_list.add(k)

        Order.objects.filter(id=order_id).update(desc=desc, level=level, date=date,end_address=end_address,remark=remark,
                                                 connect_user=connect_user,
                                                 connect_phone=connect_phone, update_order=None, price=price,
                                                )

        return ApiResponse()


# 获取所有服务类型
class GetAllServiceTypeView(GenericViewSet, ListModelMixin):
    queryset = ServiceType.objects.all()
    serializer_class = GetAllServiceTypeSerializer


# 获取所有地址
class GetAllAddressView(GenericViewSet, ListModelMixin):
    queryset = Address.objects.all()
    serializer_class = GetAllAddressSerializer


# 通过服务类型和地址查询规格品牌
class GetServiceView(APIView):
    def get(self, request):
        address_id = request.query_params.get('address_id', None)
        service_id = request.query_params.get('service_id', None)
        service_obj = None
        data_list = []
        if address_id and service_id:
            service_obj = Service.objects.filter(address_id=int(address_id), service_type_id=int(service_id)).all()

        elif address_id and not service_id:
            service_obj = Service.objects.filter(address_id=int(address_id)).all()

        elif not address_id and service_id:
            service_obj = Service.objects.filter(service_type_id=int(service_id)).all()

        for i in service_obj:
            data_list.append({'name':i.category, 'price':i.price, 'id': i.id, 'text':i.service_type.name + i.address.name + i.category})

        return ApiResponse(data=data_list)




# 更新服务
class UpdateServiceTypeView(APIView):
    def post(self,request):
        fuwu_name = request.data.get('fuwu_name', None)
        address_name = request.data.get('address_name', None)
        category_name = request.data.get('category_name', None)
        change_price = request.data.get('change_price', None)
        id = request.data.get('id', None)
        service_obj = Service.objects.filter(id=id).first()

        if fuwu_name:
            service_type_obj = ServiceType.objects.filter(name=fuwu_name).first()
            if service_type_obj:
                service_obj.service_type = service_type_obj
                service_obj.save()
            else:
                ServiceType.objects.create(name=fuwu_name)
                service_type_obj = ServiceType.objects.filter(name=fuwu_name).first()
                service_obj.service_type = service_type_obj
                service_obj.save()

        if address_name:
            address_obj = Address.objects.filter(name=address_name).first()
            if address_obj:
                service_obj.address = address_obj
                service_obj.save()
            else:
                Address.objects.create(name=address_name)
                address_obj = Address.objects.filter(name=address_name).first()
                service_obj.address = address_obj
                service_obj.save()

        if category_name:
            service_obj.category = category_name
            service_obj.save()

        if change_price:
            service_obj.price = change_price
            service_obj.save()


        return ApiResponse()

        # service_type_obj = ServiceType.objects.filter(name=name).first()

        # if service_type_obj:
        #     return ApiResponse(code=111)
        # else:
        #     new_service_type_obj = ServiceType.objects.filter(id=id).first()
        #     new_service_type_obj.name = name
        #     new_service_type_obj.save()
        #     return ApiResponse()


class CreateServiceTypeView(APIView):
    def get(self,request):
        name = request.query_params.get('name', None)

        service_type_obj = ServiceType.objects.filter(name=name).first()

        if service_type_obj:
            return ApiResponse(code=111)
        else:
            ServiceType.objects.create(name=name)

            return ApiResponse()


# 获得所有服务信息
class GetAllServiceView(GenericViewSet,ListModelMixin):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

# 创建新服务
class CreateNewServiceView(APIView):
    def post(self,request):
        service_type = request.data.get('fuwu_name2', None)
        address = request.data.get('address_name2', None)
        category = request.data.get('category_name2', None)
        price = request.data.get('new_price', None)
        service_type_obj = None
        address_obj = None

        if service_type:
            service_type_obj = ServiceType.objects.filter(name=service_type).first()
            if not service_type_obj:
                ServiceType.objects.create(name=service_type)
                service_type_obj = ServiceType.objects.filter(name=service_type).first()


        if address:
            address_obj = Address.objects.filter(name=address).first()
            if not address_obj:
                Address.objects.create(name=address)
                address_obj = Address.objects.filter(name=address).first()


        Service_obj = Service.objects.filter(service_type=service_type_obj, address=address_obj, category=category, price=price).first()
        if Service_obj:
            return ApiResponse(code=111)
        else:
            Service.objects.create(service_type=service_type_obj, address=address_obj, category=category, price=price)
            return ApiResponse()



# 删除
class DeleteView(APIView):
    def get(self,request):
        id = request.query_params.get('id', None)
        service_obj = Service.objects.filter(id=id).first()
        service_obj.delete()

        return ApiResponse()


class DeleteOrderView(APIView):

    def get(self,request):
        id = request.query_params.get('id', None)
        order_obj = Order.objects.filter(id=id).first()
        order_obj.delete()

        return ApiResponse()