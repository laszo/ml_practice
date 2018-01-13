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
