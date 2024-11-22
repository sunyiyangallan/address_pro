from rest_framework.response import Response


class ApiResponse(Response):
    def __init__(self, code=100, msg='成功', status=200, headers=None, **kwargs):
        data = {'code': code, 'msg': msg}

        if kwargs:
            data.update(kwargs)
        super().__init__(data=data, status=status, headers=headers)
