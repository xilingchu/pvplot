from paraview.simple import *
from pvplot.viewer import viewer, layout
from filter.pressure_diff_2d import pressurediff
from pathlib import Path

field     = Path('/home/xlc/DATA/gt/CRHmodel-3car-org.cgns')
pvcc_head = '/home/xlc/projects/pvplot/pvcc/pressure_2d_head.pvcc'
pvcc_tail = '/home/xlc/projects/pvplot/pvcc/pressure_2d_tail.pvcc'

# Import and filter
plot = pressurediff()
plot._import(field)
plot._filter(0)

# Set the Viewer
rviewer1 = viewer()
rviewer1.attachPlot('slice', plot.slice, 'Cell', ('Pressure',))
rviewer1.changeView(pvcc_head)

rviewer2 = viewer()
rviewer2.attachPlot('slice', plot.slice, 'Cell', ('Pressure',), is_axes=True, is_bar=True)
rviewer2.changeView(pvcc_tail)
rviewer2.setColorRange('slice', -5000, 5000)

# Set the layout
playout = layout(1612, 826)
playout.splitLayout()
playout.assignLayout(rviewer1.renderView, 1)
playout.assignLayout(rviewer2.renderView, 2)
playout.outputLayout('test.png', 5)
