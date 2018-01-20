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


_train_data_file = 'watermelon'
_test_data_file = 'watermelon'


def load(*args, **kwargs):
    file = args[0]
    data = np.loadtxt(file, dtype=np.str, delimiter=",", encoding='utf8')
    res = list()
    attrs = list(data[0])

    for line in data[1:]:
        # res.append(line)
        idx = 0
        item = {'id': idx}
        for foo in line:
            item[attrs[idx]] = foo.replace('\xa0', '')
            idx += 1
        item['label'] = 'yes' if line[-1].replace('\xa0', '') == '是' else 'no'
        res.append(item)
        # for attr in _attr_list:
        #     index = _attr_list.index(attr)
        #     item[attr] = line[index]
        # res.append(item)
        # did += 1
    return res, attrs[1:-1]

# load('car.data.txt')
