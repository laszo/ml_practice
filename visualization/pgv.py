import pygraphviz as pgv


_A = pgv.AGraph()

font_name = 'Microsoft YaHei UI'


def add_node(foo, color='blue'):
    _A.add_node(foo, fontname=font_name, color=color, shape='record')


def add_edge(foo, bar, label=None, color='green'):
    _A.add_edge(
        foo, bar, len=1.5, fontname=font_name, color=color, label=label, labelfontsize=5
    )


def show():
    _A.write('simple.dot')  # write to simple.dot
    b = pgv.AGraph('simple.dot')  # create a new graph from file
    b.layout()  # layout with default (neato)
    print(b)
    b.draw('simple.png')  # draw png
