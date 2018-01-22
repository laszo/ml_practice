from dataset.loader import get_train_data_file
import numpy as np


def get_item(tattrs, row):
    return {
        k: row[tattrs.index(k)] for k in tattrs
    }


def get_data():
    dfile = get_train_data_file()
    raw_data = np.loadtxt(dfile, dtype=np.str, delimiter=",", encoding='utf8')
    tattrs = list(raw_data[0])
    tdata = [get_item(tattrs, line) for line in raw_data[1:]]
    return tattrs, tdata


def cul_entropy(thelist):
    def p_x(x, _tlist):
        return _tlist.count(x) / len(_tlist)

    import math
    states = set(thelist)
    num = 0
    for s in states:
        px = p_x(s, thelist)
        num += px * math.log2(px)
    return 0 - num


def ta_sub_sets(ta, tdata):
    d_attr = [
        {
            ta: item[ta],
            'label': item[MAIN_ID_LABEL]
        } for item in tdata
    ]
    return d_attr


def possable_v(at, data):
    psb_va = dict()
    for item in data:
        v = item[at]
        if v not in psb_va:
            psb_va[v] = list()
        psb_va[v].append(item['label'])
    return psb_va


def xishu(v, vlist):
    return vlist.count(v) / len(vlist)


def zengyi(at, data, ent_d):

    psb_va = possable_v(at, data)
    temp_number = 0
    for pv in psb_va:
        vlist = psb_va[pv]
        ent_v = cul_entropy(vlist)
        v_xishu = len(vlist) / len(data)
        temp_number += v_xishu * ent_v
    # todo
    # import operator, functools
    # functools.reduce()
    # for 循环可以重写
    gain = ent_d - temp_number
    return gain


def zy_all(attrs, data):
    lb_all = [item[MAIN_ID_LABEL] for item in data]
    ent_d = cul_entropy(lb_all)

    res = dict()
    for at in attrs:
        taset = ta_sub_sets(at, data)
        at_zy = zengyi(at, taset, ent_d)
        res[at] = at_zy
    return res


def gooooo():
    attrs, data = get_data()
    attrs = attrs[1:-1]
    foo = zy_all(attrs, data)
    print(foo)


if __name__ == '__main__':
    MAIN_ID_LABEL = '好瓜'
    gooooo()
    pass
