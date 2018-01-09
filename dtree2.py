def get_best_arrt(tdatalist, attrlist):
    return attrlist[0]


def get_possable_values(tdatalist, arrt):
    return [getattr(tdata, arrt) for tdata in tdatalist]


class DTreeModel(object):
    def __init__(self, arrt_name=None, values=None, label=None):
        self.label = label
        self.arrt_name = arrt_name
        self.father_value = values
        self.children = []  # child is also DTreeModel


def get_label(obj):
    return obj['label']


def get_sub_data_list(tdatalist, arrt, value):
    return [
        tdata for tdata in tdatalist if getattr(tdata, arrt) == value
    ]


def get_most_label(tdatalist, attrlist):
    return attrlist[0]


def make_dtree_node(tdatalist, attrlist):
    if not tdatalist:
        return None
    if len(tdatalist) == 1:
        label = get_label(tdatalist[0])
        return DTreeModel(label=label)
    arrt = get_best_arrt(tdatalist, attrlist)
    pvalues = get_possable_values(tdatalist, arrt)
    node = DTreeModel(arrt_name=arrt, values=pvalues)
    for value in pvalues:
        subdatalist = get_sub_data_list(tdatalist, arrt, value)
        if not subdatalist:
            label = get_most_label(tdatalist, attrlist)
            return DTreeModel(label=label)
        else:
            node.children.append(make_dtree_node(subdatalist, attrlist))
    node.arrt_name = arrt
    node.possable_values = pvalues
    return node


def get_attr_list(training_data):
    return []


def train(training_data):
    attrlist = get_attr_list(training_data)
    tree = make_dtree_node(training_data, attrlist)
    return tree


def predict(model, test_data):
    return 'result'


def main():
    model = train('traindata')
    result = predict(model, 'testdata')
    predict(result)


if __name__ == '__main__':
    main()
