import visualization.pgv as pgv


_num = 0


def get_uniq_num():
    global _num
    _num += 1
    return str(_num)


def do_draw(tree):
    _draw_node(tree)
    pgv.show()


def _draw_node(node):
    if not hasattr(node, 'attr'):
        return
    pgv.add_node(node.attr)
    for chld in node.children:
        if hasattr(chld, 'children'):
            pgv.add_edge(node.attr, chld.attr, chld.father_value)
            _draw_node(chld)
        else:
            if hasattr(chld, 'label'):
                pgv.add_edge(node.attr, chld.label + get_uniq_num(), chld.father_value)
            continue
