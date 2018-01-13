import numpy as np
import os


def abs_path():
    path = os.path.abspath(__file__)
    return os.path.dirname(path)


def data_path():
    return os.path.join(abs_path(), os.pardir, 'dataset')


def get_train_data_file():
    return os.path.join(data_path(), _train_data_file)


def get_test_data_file():
    return os.path.join(abs_path(), _test_data_file)


def get_data_attrs():
    foo = list(_attr_list)
    foo.remove('label')
    return foo


_train_data_file, _test_data_file, _attr_list \
    = 'crx.data.txt', 'crx.data.txt', \
      list(range(0, 15))
_attr_list.append('label')

# car names
# [
#     'buying',
#     'maint',
#     'doors',
#     'persons',
#     'lug_boot',
#     'safety',
#     'label'
# ]


# 需要手动研究研究样例的数据，手动写出一个树来
# crx.data.txt 就似乎是一个好例子

def load(*args, **kwargs):
    file = args[0]
    data = np.loadtxt(file, dtype=np.str, delimiter=",")
    res = list()
    did = 0
    for line in data:
        item = {'id': did}
        for attr in _attr_list:
            index = _attr_list.index(attr)
            item[attr] = line[index]
        res.append(item)
        did += 1
    return res

# load('car.data.txt')
