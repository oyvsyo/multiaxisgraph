import ROOT
from array import array
import random

def arr(x):
    return array("d", x)

def set_graph_attributes(graph, color=1, line_width=1):
    try:
        graph.SetLineColor(color)
        graph.SetLineWidth(line_width)
    except Exception:
        raise UnificatedMAGError

def scale(bottom, top, min_y, max_y, default_scale=1):
    delta_x = top-bottom
    delta_y = max_y -min_y
    if delta_y == 0:
        alpha = 1/default_scale
        beta = bottom
        # y_norm = [beta  for i in range(len(y))]
    else:
        alpha = delta_x/delta_y
        beta = top-alpha*max_y
        # y_norm = [y[i]*alpha+beta  for i in range(len(y))]
    return [alpha, beta]

def range_y(ys):
    # xs structure is [[y1], [y2], ...]
    top = max(map(lambda y: max(y), ys))
    bottom = min(map(lambda y: min(y), ys))
    return [bottom, top]

def linear_transformation(a, b, y):
    return map(lambda i: a*i+b, y)


class MultiAxisGraphError(Exception):
    """Basic exception for errors raised by MultiAxisGraph"""
    def __init__(self, MAG_object, msg=None):
        if msg is None:
            msg = "An error occured with car %s" % MAG_object
        super(MultiAxisGraphError, self).__init__(msg)
        self.MAG_object = MAG_object

class UnificatedMAGError(MultiAxisGraphError):
    """docstring for UnificatedMAGError."""
    def __init__(self, msg):
        super(UnificatedMAGError, self).__init__(msg)



class MultiAxisGraph(ROOT.TObject):
    """MultiAxisGraph object allows t odraw multiple graphs and axis"""
    def __init__(self, name=None):

        super(MultiAxisGraph, self).__init__()

        if isinstance(name, str):
            self.name = name
        else:
            self.name = str(self.GetUniqueID())
        self.graphs_info = {"base":[], "right":[], "left":[]}
        self.graphs = {"base":[], "right":[], "left":[]}
        self.axis = {"left":[]}
        self.pads = []
        self.graph = ROOT.TMultiGraph()
        self.scale_coefs = {}
        # self.pad_width = 0.08
        # self.pad = ROOT.TPad("pad0_"+self.name, "pad0_"+self.name, .0, .0, 1, 1., 45, -1, -2)


    def AddGraph(self, x=[], y=[], color=1, line_width=1, mode="base"):
        """Just add info about graph, to create it when user call <Draw()> method"""
        self.graphs_info[mode] += [[x, y, color, line_width]]

    def __create_graphs(self, mode):
        """'Private' method to create ROOT.TGraph objects and add them to MAG attribute <graph>"""
        self.graphs[mode] = []
        self.graphs[mode] += [ROOT.TGraph(len(item[0]), item[0], item[1]) for item in self.graphs_info[mode]]
        n_base_graphs = len(self.graphs[mode])
        for i in range(n_base_graphs):
            set_graph_attributes(self.graphs[mode][i], self.graphs_info[mode][i][2], self.graphs_info[mode][i][3])
        map(lambda g: self.graph.Add(g), self.graphs[mode])

    def __scale(self):
        """create new info about scaled graphs"""
        self.graphs_info["right_scaled"] = []
        [bottom, top] = range_y(map(lambda item: item[1], self.graphs_info["right"]))
        [y_base_min, y_base_max] = range_y(map(lambda item: item[1], self.graphs_info["base"]))
        [a, b] = scale(y_base_min, y_base_max, bottom, top)
        self.scale_coefs["right"] = [a, b]
        # some bugs here with types in python and ROOT
        # self.graphs_info["right_scaled"] = map(lambda item: [item[0], linear_transformation(a, b, item[1]), item[2], item[3]], self.graphs_info["right"])
        # so i must add func "arr()" when setting up the data to right_scaled graphs
        self.graphs_info["right_scaled"] = map(lambda item: [arr(item[0]), arr(linear_transformation(a, b, item[1])), item[2], item[3]], self.graphs_info["right"])
        y_axis_min = self.graph.GetYaxis().GetXmin()
        y_axis_max = self.graph.GetYaxis().GetXmax()
        x_axis_max = self.graph.GetXaxis().GetXmax()

        self.axis["right"] = ROOT.TGaxis(x_axis_max,
                                         y_axis_min,
                                         x_axis_max,
                                         y_axis_max,
                                         (y_axis_min-b)/a,
                                         (y_axis_max-b)/a,
                                         510,
                                         "+L")


    def SetTitle(self, title=0):
        """use this to set graph title"""
        try:
            self.graph.SetTitle(title)
        except Exception:
            raise UnificatedMAGError

    def __str__(self):
        return "MultiAxisGraph object - %s " %self.name

    def __repr__(self):
        return "<MultiAxisGraph object at 0x%0x>" %id(self)

    def __enter__(self):
        return self

    def __exit__(self):
        """delete ROOT.TObject when program exit"""
        delete(super(MultiAxisGraph, self))

    def Draw(self):
        """Create all needed objects and draw them all """
        self.__create_graphs("base")
        self.graph.Draw("AL")
        ROOT.gPad.Update()
        if len(self.graphs_info["right"])!=0:
            self.__scale()
            self.__create_graphs("right_scaled")
            self.graph.Draw("AL")
            self.axis["right"].Draw()
            ROOT.gPad.Update()


x_t = arr(range(18))
x_u = arr(range(18))
x_i = arr(range(18))
y_t = arr(random.sample(range(20), 18))
y_u = arr(random.sample(range(20), 18))
y_i = arr(random.sample(range(20, 40, 1), 18))

c = ROOT.TCanvas()

s = MultiAxisGraph()
s.SetTitle("test MultiAxisGraph")
s.AddGraph(x_t, y_t)
s.AddGraph(x_i, y_i, color=3, mode="right")
s.Draw()
