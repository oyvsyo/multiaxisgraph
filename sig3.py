import ROOT
from array import array
import random

def arr(x):
    return array("d", x)

def set_graph_attributes(graph, n_points=0, x=[], y=[], title="graph title", color=1, line_width=1):
    graph.Set(n_points)
    # print "in function set_graph_attributes n = ", graph.GetN()
    map(lambda i: graph.SetPoint(i, x[i], y[i]), range(n_points))
    graph.SetTitle(title)
    graph.SetLineColor(color)
    graph.SetLineWidth(line_width)

# def set_axis_attributes(axis, x1, y1, x2, y2, , ):



class SuperImposiveGraph3(ROOT.TObject):

    def __init__(self, name=None):

        super(SuperImposiveGraph3, self).__init__()

        if isinstance(name, str):
            print "isinstance(name, str) = ", isinstance(name, str)
        else:
            self.name = str(self.GetUniqueID())
        self.pad_width = 0.08
        self.pad0 = ROOT.TPad("pad0_"+self.name, "pad0_"+self.name, .0, .0, self.pad_width, 1., 45, -1, -2)
        self.pad1 = ROOT.TPad("pad1_"+self.name, "pad1_"+self.name, self.pad_width, 0., self.pad_width*2, 1., 56, -1, -2)
        self.pad2 = ROOT.TPad("pad2_"+self.name, "pad2_"+self.name, self.pad_width*2, .0, 1., 1., 78, -1, -2)
        self.hist = ROOT.TH2F("h_"+self.name, "h_"+self.name, 1, 1, 10, 1, 1, 10)
        self.graph1 = ROOT.TGraph()
        self.graph2 = ROOT.TGraph()
        self.graph3 = ROOT.TGraph()
        self.axis_pad0 = ROOT.TGaxis()
        self.axis_pad1 = ROOT.TGaxis()


    def set_graph1(self, x=[], y=[], title="graph title", color=1, line_width=1):
        set_graph_attributes(self.graph1, len(x), x, y, title, color, line_width)
        self.hist.SetTitle(title)
        # print "len(x) ", len(x)
        self.hist.GetXaxis().SetRangeUser(min(x), max(x))
        self.hist.GetYaxis().SetRangeUser(min(y),max(y))

    def set_graph2(self, x=[], y=[], title="graph title", color=1, line_width=1):
        set_graph_attributes(self.graph2, len(x), x, y, title, color, line_width)
        # print "in function set_graph_attributes n = ", self.graph2.GetN()

    def set_graph3(self, x=[], y=[], title="graph title", color=1, line_width=1):
        set_graph_attributes(self.graph3, len(x), x, y, title, color, line_width)

    def __str__(self):
        return "class SuperImposiveGraph3 - %s" %self.name

    def __repr__(self):
        return "<SuperImposiveGraph3 object at 0x%0x>" %id(self)

    def __enter__(self):
        return self

    def __exit__(self):
        delete(super(SuperImposiveGraph3, self))

    def Draw(self):
        # ROOT.gPad.cd()
        self.pad0.Draw()
        self.pad1.Draw()
        self.pad2.Draw()
        self.pad2.cd()
        self.pad2.SetRightMargin(0.01)
        self.pad2.SetLeftMargin(0.12)

        self.hist.SetStats(ROOT.kFALSE)
        # self.hist.GetXaxis().SetTitle(self.name)
        self.hist.Draw()

        # self.pad2.Update()
        self.graph1.Draw()
        self.pad2.Update()
        self.graph2.Draw()
        self.pad2.Update()
        self.graph3.Draw()
        self.pad2.Update()

x_t = arr(range(18))
x_u = arr(range(10))
x_i = arr(range(20))
y_t = arr(random.sample(range(20), 18))
y_u = arr(random.sample(range(20), 10))
y_i = arr(random.sample(range(20), 20))

c = ROOT.TCanvas()

s = SuperImposiveGraph3()

s.set_graph1(x_t, y_t, "gaph1",)

s.set_graph2(x_i, y_i, "graph2", color=6)

s.set_graph3(x_u, y_u, "graph3", color=9)

s.Draw()
