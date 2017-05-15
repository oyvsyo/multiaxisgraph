# MultiAxisGraph class

## Introduction
This is the python class, that use ROOT framework to make data vizualization easier.
The main function - draw different values in one frame, without carring about ranges and additional axises. This is especially useful when you need to display the dependence of different values from one value.

## Requirements
* ROOT 5.xx
* python 2 with ROOT enabled

## Example
MultiAxisGraph is realy 'DoubleAxisGraph', so multiple axises is in development.
This class interface allows you to compose graphs (ROOT.TGraph) and setting up axises for them (on this moment only two).
Usage of MultiAxisGraph (MAG) object can be divided into the following stages:
* Creating TGraphs objects & setting their properties
* Adding TGraph objects to MultiAxisGraph & draw MAG object
* Getting MAG attributes & setting up their properties
* Update pad

Run the following example by `$ python2 -i example.py`

```
import ROOT
import mag

# setting up data samples
# mag.arr() function uses for setting up a double type to numbers in sample list
x1 = mag.arr(range(100))
x2 = mag.arr(map(lambda i: i/5., range(500)))
y1 = mag.arr(map(lambda i: i**0.5, x1))
y2 = mag.arr(map(lambda i: ROOT.TMath.Sin(i), x2))
c = ROOT.TCanvas()

# create graphs from data samples & setting up some properties
gr1 = ROOT.TGraph(len(x1), x1, y1)
gr1.SetTitle("y = #sqrt{x}")
gr1.SetLineWidth(2)
gr2 = ROOT.TGraph(len(x2), x2, y2)
gr2.SetTitle("y = sin(x)")
gr2.SetLineWidth(2)
gr2.SetLineColor(2)

# create MultiAxisGraph object
MAG = mag.MultiAxisGraph()
# adding graphs to mag object
# mode "right" means, that graph will be scaled and represented with right axis
MAG.AddGraph(gr1)
MAG.AddGraph(gr2, mode="right")
# draw the mag object
MAG.Draw()

# accses to multigraph object in mag for setting style and attributes
mlt_graph = MAG.GetMultigraph()
mlt_graph.GetYaxis().SetTitle("axis for #sqrt{x} graph")
mlt_graph.GetXaxis().SetTitle("x")

# accses to rigth axis for setting it's attributes
rigth_axis = MAG.GetRightAxis()
rigth_axis.SetTitle("axis for sin(x) graph")
rigth_axis.SetLineColor(2)
rigth_axis.SetLabelFont(42)
rigth_axis.SetTitleFont(42)
# update the canvas so changes is applied
c.Update()
```

After executing example you will get the canvas:

![alttext](https://raw.githubusercontent.com/oyvsyo/multiaxisgraph/master/example.jpg)

## License
