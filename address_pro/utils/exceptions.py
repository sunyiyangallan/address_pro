from rest_framework.views import exception_handler
from rest_framework.response import Response

# 用这个配置文件的好处：无论你是开发阶段，还是上线阶段，取到的都是当前项目运行使用的配置文件
# 项目配置文件如果没写，会有默认的配置文件
from django.conf import settings
from utils.loggings import logger
def common_exception_handler(exc, context):
    # 只要走到这，说明程序出异常了，都需要记录日志，越详细越好
    request=context.get('request')
    view=context.get('view')
    ip=request.META.get('REMOTE_ADDR')
    path=request.path
    logger.error('程序出错了，错误视图类是：%s，用户ip是：%s，请求地址是：%s,错误原因：%s'%(str(view),ip,path,str(exc)))


    # 只处理了drf的异常，如果res有值，就是drf的异常，处理了，如果为None，就是djagno的异常，我们额外处理
    res = exception_handler(exc, context)
    if settings.DEBUG:
        if res:
            return Response({'code': 888, 'msg': res.data['detail']})
        else:
            return Response({'code': 999, 'msg': str(exc)})
    else:
        return Response({'code': 999, 'msg': '系统错误，请联系系统管理员'})