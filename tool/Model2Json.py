from datetime import datetime


class Model2Json(object):
    def o2d(self):
        return {k: v for k, v in self.__dict__.items() if
                not str(k).startswith('_')}

    def validate(self):
        raise Exception("unimplement method")

    @staticmethod
    def json_dumps_default(obj):
        """
        json.dumps()方法中，python对象转换为json对象的default方法
        本接口对于嵌套python对象也有效
        """
        if hasattr(obj, 'o2d'):
            return obj.o2d()
        else:
            if isinstance(obj, datetime):
                return int(obj.timestamp() * 1000)
            if isinstance(obj, bytes):
                return None
            return obj
