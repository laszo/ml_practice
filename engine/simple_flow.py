from dataset.loader import load as loaddata
from dataset.loader import get_train_data_file, get_test_data_file, get_data_attrs
from engine.dtree2 import make_dtree_node, predict_data
from tool import attr_value


def test_result(item):
    return attr_value(item, 'label') == attr_value(item, 'predict_label')


def get_result_rate(result):
    badres = [
        item for item in result if not test_result(item)
    ]
    return len(badres) / len(result)


def run_the_flow():
    train_data = loaddata(get_train_data_file())
    attrs = get_data_attrs()
    dtree = make_dtree_node(train_data, attrs)
    test_data = loaddata(get_test_data_file())
    result = predict_data(dtree, test_data)
    rate = get_result_rate(result)
    print(rate)
    return result


if __name__ == '__main__':
    run_the_flow()
