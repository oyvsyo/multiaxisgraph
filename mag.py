import ROOT
from array import array
from copy import deepcopy

def arr(x):
    return array("d", x)

def set_graph_attributes(graph, color=1, line_width=1, name="", title=""):
    try:
        graph.SetLineColor(color)
        graph.SetLineWidth(line_width)
        if title:
            graph.SetTitle(title)
        if name:
            graph.SetName(name)
    except Exception:
        raise UnificatedMAGError

def set_graph_y(graph, y):
    gety = graph.GetY()
    for i in range(graph.GetN()):
        gety[i] = y[i]

def get_graph_y(graph):
    gety = graph.GetY()
    return map(lambda i: gety[i], range(graph.GetN()))

def add_graphs(multigraph, graphs):
    map(lambda g: multigraph.Add(g), graphs)

def scale(bottom, top, min_y, max_y, default_scale=1):
    delta_x = top-bottom
    delta_y = max_y -min_y
    if delta_y == 0:
        alpha = 1/default_scale
        beta = bottom
    else:
        alpha = delta_x/delta_y
        beta = top-alpha*max_y
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
        self.graphs = {"base":[], "right":[], "left":[]}
        self.axis = {"left":[], "right":[]}
        self.pads = []
        self.graph = ROOT.TMultiGraph()
        self.scale_coefs = {}

    def GetMultigraph(self,):
        return self.graph

    def GetBaseGraphs(self):
        """return a list of base graphs"""
        return self.graphs["base"]

    def GetRightGraphs(self):
        """return a list of right graphs"""
        return self.graphs["right"]

    def GetLeftGraphs(self):
        """return a list of left graphs"""
        return self.graphs["left"]

    def GetRightAxis(self):
        return self.axis["right"]

    def AddGraph(self, graph, mode="base"):
        """Write graph to 909"""
        self.graphs[mode] += [graph]

    def __scale(self):
        """create new info about scaled graphs"""
        [bottom, top] = range_y(map(lambda graph: get_graph_y(graph), self.graphs["right"]))
        [y_base_min, y_base_max] = range_y(map(lambda graph: get_graph_y(graph), self.graphs["base"]))
        [a, b] = scale(y_base_min, y_base_max, bottom, top)
        self.scale_coefs["right"] = [a, b]
        # some bugs here with types in python and ROOT
        # self.graphs_info["right_scaled"] = root copymap(lambda item: [item[0], linear_transformation(a, b, item[1]), item[2], item[3]], self.graphs_info["right"])
        # so i must add func "arr()" when setting up the data to right_scaled graphs
        self.graphs["right_scaled"] = deepcopy(self.graphs["right"])
        n = len(self.graphs["right"])
        # for i in range(n):
        #     y = linear_transformation(a, b, get_graph_y(self.graphs["right"][i]))
        #     set_graph_y(self.graphs["right_scaled"][i], y)
        #     # y_new = get_graph_y(self.graphs["right_scaled"][i])
        #     print y
        map(lambda i: set_graph_y(self.graphs["right_scaled"][i], linear_transformation(a, b,get_graph_y(self.graphs["right"][i]))), range(n))
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
        add_graphs(self.graph, self.graphs["base"])
        self.graph.Draw("AL")
        if len(self.graphs["right"])!=0:
            self.__scale()
            add_graphs(self.graph, self.graphs["right_scaled"])
            self.graph.Draw("AL")
            self.axis["right"].Draw()
        ROOT.gPad.Update()

    def Update(self):
        self.graph.Draw("AL")
        if len(self.graphs_info["right"])!=0:
            self.axis["right"].Draw()
        ROOT.gPad.Update()


ROOT.gRandom.SetSeed()
rndm = ROOT.gRandom.Rndm

x = arr(range(100))
y_t = arr(map(lambda i: i*rndm(1)+47., x))
y_u = arr(map(lambda i: i**0.5+rndm(2), x))
y_i = arr(map(lambda i: ROOT.TMath.Sin(i), x))

c = ROOT.TCanvas()

s = MultiAxisGraph()

gr1 = ROOT.TGraph(len(x), x, y_t)
gr2 = ROOT.TGraph(len(x), x, y_u)
gr2.SetLineColor(9)
gr3 = ROOT.TGraph(len(x), x, y_i)
gr3.SetLineColor(9)


s.AddGraph(gr1)
s.AddGraph(gr2, mode="right")
s.AddGraph(gr3, mode="right")

s.Draw()

mlt_graph = s.GetMultigraph()
mlt_graph.SetTitle("test MultiAxisGraph")

rigth_axis = s.GetRightAxis()
rigth_axis.SetTitle("rigth axis")
rigth_axis.SetLineColor(9)
rigth_axis.SetLabelFont(42)
rigth_axis.SetTitleFont(42)

c.Update()
