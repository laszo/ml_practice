import matplotlib.pyplot as plt


ax1 = None

tnode_style = dict(boxstyle="round4", fc="1")  # 定义判断节点形态
leafNode = dict(boxstyle="round4", fc="1")  # 定义叶节点形态
arrow_args = dict(arrowstyle="-")  # 定义箭头
plt.interactive(True)


def draw_text_node(x, y, text):
    ax1.text(x, y, text, va="center", ha="left", wrap=True, bbox=tnode_style)


def center_pt(pt1, pt2):
    subx = pt1[0] + (pt2[0] - pt1[0]) / 2
    suby = pt1[1] + (pt2[1] - pt1[1]) / 2
    return subx, suby


def offset_pt(pt, x=0, y=0):
    return pt[0] + x, pt[1] + y


def arrow(pt1, pt2, text):
    center = center_pt(pt1, pt2)
    ax1.annotate(
        text, xy=pt1, va="center", ha="center", xytext=center, arrowprops=arrow_args,
        xycoords='data', textcoords='data'
    )
    ax1.annotate(
        '', xy=center, va="center", ha="center", xytext=pt2, arrowprops=arrow_args,
        xycoords='data', textcoords='data'
    )


def draw_tree(model, maxd, maxw, node_num_dict):
    global ax1
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=list(range(0, maxw)), yticks=list(range(0, maxd * 2)))
    ax1 = plt.subplot(111, frameon=False, **axprops)
    ax1.autoscale(False)
    plt.interactive(True)
    plt.axis('on')
    plt.show()
    _real_draw(model, maxd, maxw, node_num_dict)


def _real_draw(model, maxd, maxw, node_num_dict, father_child_count=0, father_x=0):
    # print(model)
    curw = node_num_dict[model.x] - 1
    x = model.x * 1.0
    if father_child_count == 0:
        x = (maxw-1) / 2
    else:
        x = father_x + (model.index_in_father - father_child_count / 2)
        # todo 这里搞了一点点。基本思路是让子节点的x坐标，基于父节点的x坐标加上或减去一个值
        # todo 应该让子节点多的节点放在中间
    # x = model.x * 1.0 / curw * maxw
    y = model.y * 1.0
    text = model.attr_name if model.attr_name else model.label
    print('node:', x, y, text)
    draw_text_node(x, y, text)
    for child in model.children:
        cx = child.x * 1.0
        cx = cx + (child.index_in_father - len(model.children) / 2)
        cy = child.y * 1.0
        px = x
        py = y
        # draw_arrow((x, y), child.father_value, (child.x, child.y))
        print('arrow', px, py, cx, cy, child.father_value)
        arrow((cx, cy), (px, py), child.father_value)
        _real_draw(child, maxd, maxw, node_num_dict, len(model.children), x)
