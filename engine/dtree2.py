from engine.dtree_base import *


def get_best_arrt_old(tdata, attrs):
    bestattr = attrs[0]
    return bestattr


def getpair(x, y):
    return x, y


def get_best_arrt(tdatalist, attrlist):
    bestattr = attrlist[0]
    maxrate = 0

    for attr in attrlist:

        label_count_dict = dict()
        for data in tdatalist:
            value = attr_value(data, attr)
            label = get_label(data)
            pair = getpair(value, label)
            if pair not in label_count_dict:
                label_count_dict[pair] = 1
            else:
                label_count_dict[pair] += 1
        all_labels = uniquelist(label_count_dict.keys())
        max_label = all_labels[0]
        max_count = label_count_dict[max_label]
        for pair in label_count_dict.keys():
            if max_count < label_count_dict[pair]:
                max_label = pair
                max_count = label_count_dict[pair]

        crate = max_count / len(tdatalist)
        # print(tdatalist, attrlist)
        print(max_label, crate)

        if maxrate < crate:
            maxrate = crate
            bestattr = attr
    return bestattr


def get_most_label(tdata, attrs):
    return get_label(tdata[0])


def get_children(attrs, battr, tdata):
    children = list()
    pvalues = get_possable_values(tdata, battr)
    sub_datas_list = list()  # it is m*n matrix, not just a list.
    for v in pvalues:
        # 把tdata根据不同的v划分为多个子subdata
        subdata = [item for item in tdata if attr_value(item, battr) == v]
        sub_datas_list.append((v, subdata))
    for v, subdata in sub_datas_list:
        if len(subdata) == 0:
            label = get_most_label(tdata)
            child = DTreeLeaf(label, v)
        elif len(subdata) == 1:
            child = DTreeLeaf(get_label(subdata[0]), v)
        else:
            child = make_dtree_node(subdata, attrs)
        if child:
            child.father_value = v
            children.append(child)
    return children


def make_dtree_node(tdata, attrs):
    if len(attrs) > 1:
        battr = get_best_arrt(tdata, attrs)
        node = DTreeNode(battr)
        attrs.remove(battr)
        node.children = get_children(attrs, battr, tdata)
        return node
    label = get_most_label(tdata, attrs)
    node = DTreeLeaf(label)
    return node


def predict(model, item):
    if isinstance(model, DTreeLeaf):
        return model.label
    for child in model.children:
        if child.father_value == attr_value(item, model.attr):
            label = predict(child, item)
            return label


def predict_data(tree, data):
    return [
        {
            'predict_label': predict(tree, item),
            'label': get_label(item),
            'id': attr_value(item, 'id')
        }
        for item in data
    ]
