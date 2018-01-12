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


def get_simple_traindata():
    return [
        {'age': item[0], 'height': item[1], 'label': item[2], 'name': item[3]}
        for item in [
            (18, 159, 'no', 'juccy'),
            (19, 169, 'ok', 'candy'),
            (18, 179, 'ok', 'lucy'),
            (28, 165, 'ok', 'modona'),
            (38, 168, 'no', 'ladyy')
        ]
    ]


def read_csv_file(filename):
    res = list()
    with open(filename) as of:
        lines = of.readlines()
        if lines:
            for row in lines:
                item = row.split(',')
                model = get_simple_model(item)
                if model:
                    res.append(model)
    return res


def get_simple_model(row):
    if isinstance(row, list):
        res = dict()
        # res['id'] = row[-2]
        res['label'] = row[-1].replace('\n', '')
        number = 0
        attrlist = ['Color', 'size', 'act', 'age']
        for item in row[:-1]:
            # res['attr_%d' % number] = item
            res[attrlist[number]] = item
            number += 1
        return res


def get_traindata():
    return read_csv_file('dataset/adult+stretch.data.txt')
    # return read_csv_file('dataset/audiology.standardized.data')
    # return read_csv_file('dataset/audiology.standardized.data_dummy1')
    # return read_csv_file('dataset/bridges.data.version1.txt')


def get_testdata():
    return read_csv_file('dataset/adult+stretch.data.txt')
    # return read_csv_file('dataset/audiology.standardized.test')
    # return read_csv_file('dataset/audiology.standardized.test_dummy1')
    # return read_csv_file('dataset/bridges.data.version1.txt')
