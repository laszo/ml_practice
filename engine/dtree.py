import json

from drawhelper import draw_tree
from thedata import get_traindata, Model2Json, get_testdata


def attr_value(obj, attr):
    if isinstance(obj, dict):
        return obj[attr]
    raise Exception('at attr_value: obj is not a dict')


def get_label(obj):
    return attr_value(obj, 'label')


def uniquelist(listobj):
    return list(set(listobj))


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


def get_possable_values(tdatalist, arrt):
    return uniquelist([attr_value(tdata, arrt) for tdata in tdatalist])


def get_sub_data_list(tdatalist, arrt, value):
    return [
        tdata for tdata in tdatalist if attr_value(tdata, arrt) == value
    ]


def get_most_label(tdatalist, attrlist):
    return get_label(tdatalist[0])


node_num_dict = dict()


class DTreeModel(Model2Json):
    def __init__(self, depth, attr_name=None, label=None):
        self.label = label
        self.attr_name = attr_name
        self.father_value = None
        self.father_attr_name = None
        self.children = []  # child is also DTreeModel
        self.y = depth
        if depth not in node_num_dict:
            node_num_dict[depth] = 0
        self.x = node_num_dict[depth]
        node_num_dict[depth] += 1
        global max_width
        if max_width < node_num_dict[depth]:
            max_width = node_num_dict[depth]
        self.index_in_father = 0

    def newick_text(self):
        if self.children:
            return '(%s)' % ','.join([child.newick_text() for child in self.children if child and child.newick_text()])
        return self.attr_name


    def __repr__(self):
        return json.dumps(self, default=Model2Json.json_dumps_default)


max_depth = 0
max_width = 0


def make_dtree_node(tdatalist, pre_attrlist, depth=0):
    global max_depth
    global max_width
    # print(pre_attrlist)
    # print(len(tdatalist))
    if not tdatalist:
        return None
    if len(tdatalist) == 1:
        label = get_label(tdatalist[0])
        node = DTreeModel(depth, label=label)
        return node
    battr = get_best_arrt(tdatalist, pre_attrlist)
    pvalues = get_possable_values(tdatalist, battr)
    node = DTreeModel(depth, attr_name=battr)
    if max_depth < depth:
        max_depth = depth
    pre_attrlist.remove(battr)
    index_in_father = 0
    for value in pvalues:
        subdatalist = get_sub_data_list(tdatalist, battr, value)
        if not subdatalist or not pre_attrlist:
            label = get_most_label(tdatalist, pre_attrlist)
            child = DTreeModel(depth + 1, label=label)
        else:
            child = make_dtree_node(subdatalist, pre_attrlist, depth + 1)
        if child:
            child.father_value = value
            child.father_attr_name = battr
            child.index_in_father = index_in_father
            node.children.append(child)
            index_in_father += 1
    return node


def get_attr_list(training_data):
    attr_list = list()
    for tdata in training_data:
        fk = set(tdata.keys())
        attr_list.extend(fk)
    return list(set(attr_list))


def train(training_data):
    attrlist = get_attr_list(training_data)
    try:
        attrlist.remove('label')
        attrlist.remove('id')
    except:
        pass
    pre_attr_list = list(attrlist)
    tree = make_dtree_node(training_data, pre_attr_list)
    return tree


def predict(model, item):
    if model.label:
        return model.label
    for child in model.children:
        if child.father_value == attr_value(item, model.attr_name):
            label = predict(child, item)
            return label


def train_dtree(data):
    return ''


def predict_data(tree, data):
    return [
        {
            'label': predict(tree, item),
            'id': attr_value(item, 'id')
        }
        for item in data
    ]


def main():
    traindata = get_traindata()
    model = train(traindata)
    # print(model)
    # print('max_depth: %d' % max_depth)
    # print('max_width: %d' % max_width)
    draw_tree(model, max_depth, max_width, node_num_dict)
    testdata = get_testdata()
    right_num = 0
    wrong_num = 0
    all_num = 0
    for test_item in testdata:
        label = predict(model, test_item)
        if label == get_label(test_item):
            right_num += 1
        else:
            wrong_num += 1
        all_num += 1
    print(right_num / all_num)
    print(model.newick_text())
    pass


if __name__ == '__main__':
    main()
    # ttttraindata = get_traindata()
    # mmmmmodel = train(ttttraindata)
    # draaaaaw(mmmmmodel)

    # discover_draw()
    # plt.show()
