import ROOT
from array import array
import random

def arr(x):
    return array("d", x)

def set_graph_attributes(color=1, line_width=1):
    graph.SetLineColor(color)
    graph.SetLineWidth(line_width)

def scale(bottom, top, y, default_scale=1):
    delta_x = top-bottom
    delta_y = max(y)-min(y)
    if delta_y == 0:
        alpha = 1/default_scale
        beta = bottom
        y_norm = [beta  for i in range(len(y))]
    else:
        alpha = delta_x/delta_y
        beta = top-alpha*max(y)
        y_norm = [y[i]*alpha+beta  for i in range(len(y))]
    return [alpha, beta, arr(y_norm)]

# def set_axis_attributes(axis, x1, y1, x2, y2, , ):

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

    def __init__(self, name=None):

        super(MultiAxisGraph, self).__init__()

        if isinstance(name, str):
            self.name = name
        else:
            self.name = str(self.GetUniqueID())
        self.pad_width = 0.08
        self.pad = ROOT.TPad("pad0_"+self.name, "pad0_"+self.name, .0, .0, 1, 1., 45, -1, -2)
        self.graph = ROOT.TMultiGraph()
        self.right_axis = 0
        self.axis = []
        self.pads = []
        self.graphs = []
        self.bottom = +99999999.
        self.top = -99999999.

    def AddGraph(self, x=[], y=[], color=1, line_width=1, use_axis=0):
        self.AddBaseGraph(x, y, color, line_width)
        if use_axis==1:
            k = len(self.pads)
            self.pads += ROOT.TPad()
            self.axis += ROOT.TGaxis()
        if use_axis==-1:
            max_x = max(x)
            [alpha, beta, y_scale] = scale(self.bottom, self.top, y)
            self.right_axis = ROOT.TGaxis(max_x, 0.1, max_x, 0.9, )


    def AddBaseGraph( x=[], y=[], color=1, line_width=1,):
        self.graphs += ROOT.TGraph(len(x), x, y)
        i = len(self.graphs)-1
        self.graphs[i].SetName("graph_%i" %i)
        if self.bottom > min(y):
            self.bottom = min(y)
        if self.top < max(y):
            self.top = max(y)
        set_graph_attributes(self.graphs[i], color, line_width)

    def SetPads(self):
        k = len(self.pads)
        self.pad_width = 1-0.5/(k+1)
        self.pad.SetPad(pad_width, 0., 0., 1.)
        map(lambda p: p.SetPad((1-self.pad_width)))

    def SetTitle(self, title=0):
        try:
            self.graph.SetTitle(title)
        except Exception:
            raise UnificatedMAGError

    def __str__(self):
        return "class MultiAxisGraph - %s" %self.name

    def __repr__(self):
        return "<MultiAxisGraph object at 0x%0x>" %id(self)

    def __enter__(self):
        return self

    def __exit__(self):
        delete(super(MultiAxisGraph, self))

    def Draw(self):
        map(lambda pad_item: pad_item.Draw, self.pads)
        self.pad.Draw()
        self.pad.cd()
        self.pad.SetRightMargin(0.01)
        self.pad.SetLeftMargin(0.12)



x_t = arr(range(18))
x_u = arr(range(10))
x_i = arr(range(20))
y_t = arr(random.sample(range(20), 18))
y_u = arr(random.sample(range(20), 10))
y_i = arr(random.sample(range(20), 20))

c = ROOT.TCanvas()

s = MultiAxisGraph()
# sig.set_graph1()
# s.AddGraph(x_t, y_t)
#
# s.AddGraph(x_i, y_i)
#
# s.AddGraph(x_u, y_u)
#
s.Draw()
# c2 = ROOT.TCanvas()
# sig2 = MultiAxisGraph("kek")
# sig2.Draw()
