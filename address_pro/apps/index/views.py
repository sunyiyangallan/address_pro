from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from utils.response import ApiResponse
from address_pro.utils.md5 import md5_encrypt
from .models import AddressUser, BaseSettings, Order
from .serializer import GetLoginImgSerializer, GetJueSeSerializer, GetUserInfoSerializer, GetAllOrderSerializer, \
    GetUserSerializer, GetOneOrderSerializer
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
    search_fields = ['desc', 'uuid', ]

    def get_queryset(self):
        # 定义状态的排序顺序
        state_order = Case(
            When(state=1, then=0),
            When(state=0, then=1),
            When(state=2, then=2),
        )

        # 获取基础查询集并应用排序和过滤
        queryset = Order.objects.all().annotate(state_order=state_order).order_by('state_order', 'id')

        # 筛选 user 字段未赋值的订单
        queryset = queryset.filter(user__isnull=False)
        return queryset



class GetUserOrderView(GenericViewSet, ListModelMixin):
    # queryset = Order.objects.all().order_by('date')
    serializer_class = GetAllOrderSerializer
    filter_backends = [SearchFilter]
    search_fields = ['user__token', 'desc', 'uuid', ]


    def get_queryset(self):
        # 定义状态的排序顺序
        state_order = Case(
            When(state=1, then=0),
            When(state=0, then=1),
            When(state=2, then=2),
        )

        # 获取基础查询集并应用排序和过滤
        queryset = Order.objects.all().annotate(state_order=state_order).order_by('state_order', 'id')
        return queryset



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
            {'value': count3, 'name': '管理员'},
            {'value': count1, 'name': '送货员'},
            {'value': count2, 'name': '派单员'},
        ]

        return ApiResponse(data=data)


# 获取总订单状态数据
class GetOrderStateView(APIView):
    def get(self, request):
        count1 = Order.objects.filter(state=0).count()
        count2 = Order.objects.filter(state=1).count()
        count3 = Order.objects.filter(state=2).count()

        data = [
            {'value': count1, 'name': '未开始'},
            {'value': count2, 'name': '进行中'},
            {'value': count3, 'name': '已完成'},
        ]

        return ApiResponse(data=data)


# 获取所有的送货员
class GetAllCommonUserView(GenericViewSet, ListModelMixin):
    queryset = AddressUser.objects.filter(juese=0).all()
    serializer_class = GetUserSerializer


# 创建订单
class CreateOrderView(APIView):
    def post(self, request):
        # user_id = request.data.get('user')
        # user_obj = AddressUser.objects.filter(id=user_id).first()

        desc = request.data.get('desc')
        level = int(request.data.get('level'))
        # date = request.data.get('time3')

        date = datetime.strptime(request.data.get('time3'), '%Y-%m-%dT%H:%M:%S.%fZ')
        # start_address = request.data.get('search_start')
        end_address = request.data.get('search_end')
        num = request.data.get('search_num')
        # start_location = request.data.get('start_location')
        # end_location = request.data.get('end_location')
        # start_time = request.data.get('time1')
        # start_time = datetime.strptime(request.data.get('time1'), '%Y-%m-%dT%H:%M:%S.%fZ')

        Order.objects.create( desc=desc, level=level, date=date,end_address=end_address,num=num)

        return ApiResponse()


class GetOneOrderView(GenericViewSet, ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = GetOneOrderSerializer
    filter_backends = [SearchFilter]
    search_fields = ['id', ]


class StartOrderView(APIView):
    def get(self,request):
        id = request.query_params.get('id')
        Order.objects.filter(id=id).update(state=1,start_time=datetime.now())
        return ApiResponse()


class EndOrderView(APIView):
    def get(self, request):
        id = request.query_params.get('id')
        Order.objects.filter(id=id).update(state=2,end_time=datetime.now())
        return ApiResponse()



class NullOrderView(GenericViewSet,ListModelMixin):
    queryset = Order.objects.filter(user__isnull=True).all()
    serializer_class = GetAllOrderSerializer

# 更新订单
class UpdateOrderView(APIView):
    def post(self,request):
        user = request.data.get('user')
        order = request.data.get('order')

        user_obj = AddressUser.objects.filter(id=user).first()
        Order.objects.filter(id=order).update(user=user_obj)

        return ApiResponse()
