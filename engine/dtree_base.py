from tool import attr_value, uniquelist, get_label
from tool.Model2Json import Model2Json


class DTreeNode(Model2Json):
    def __init__(self, attr):
        self.attr = attr
        self.father_value = None
        self.children = []  # child is DTreeNode or DTreeLeaf


class DTreeLeaf(Model2Json):
    def __init__(self, label, father_value=None):
        self.label = label
        self.father_value = father_value


def get_possable_values(tdata, arrt):
    return uniquelist([attr_value(item, arrt) for item in tdata])
