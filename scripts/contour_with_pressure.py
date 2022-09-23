from paraview.simple import *

# V13 Best Bound CGNS
v13_best_boundcgns = CGNSSeriesReader(registrationName='V13_best_bound.cgns', FileNames=['/home/xlc/DATA/gt/gt/V13_best_bound.cgns'])
v13_best_boundcgns.Bases = ['Base']
v13_best_boundcgns.CellArrayStatus = ['Pressure', 'SkinFriction', 'WallShearStressMagnitude']
# V13 Best CGNS
v13_bestcgns       = CGNSSeriesReader(registrationName='V13_best.cgns'      , FileNames=['/home/xlc/DATA/gt/gt/V13_best.cgns'])
v13_bestcgns.Bases = ['Base']
v13_bestcgns.CellArrayStatus       = ['Qcriterion', 'Velocity']

# create a new 'Cell Data to Point Data'
cellDatatoPointData1 = CellDatatoPointData(registrationName='CellDatatoPointData1', Input=v13_bestcgns)
cellDatatoPointData1.CellDataArraytoprocess = ['Qcriterion', 'Velocity']

# create a new 'Contour'
contour1 = Contour(registrationName='Contour1', Input=cellDatatoPointData1)
contour1.ContourBy = ['POINTS', 'Qcriterion']
contour1.Isosurfaces = [10]

# Set the view
# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
v13_best_boundcgnsDisplay = Show(v13_best_boundcgns, renderView1, 'UnstructuredGridRepresentation')
 
contour1Display           = Show(contour1, renderView1, 'GeometryRepresentation')

# Set the scalar color
ColorBy(v13_best_boundcgnsDisplay, ('CELLS', 'Pressure'))

# Set the scalar color
ColorBy(contour1Display, ('Points', 'Velocity'))

# show color bar/color legend
v13_best_boundcgnsDisplay.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'Pressure'
pressureLUT = GetColorTransferFunction('Pressure')

# get opacity transfer function/opacity map for 'Pressure'
pressurePWF = GetOpacityTransferFunction('Pressure')

# Properties modified on pressurePWF
pressurePWF.Points = [-5000.0, 0.0, 0.5, 0.0, 5000.0, 1.0, 0.5, 0.0]

# Properties modified on pressureLUT
pressureLUT.RGBPoints = [-5000.0, 0.231373, 0.298039, 0.752941, 5000.0, 0.705882, 0.0156863, 0.14902]

# trace defaults for the display properties.
# v13_best_boundcgnsDisplay.Representation = 'Surface'
 
# v13_bestcgnsDisplay.Representation       = 'Surface'
#-----------------------------------------#
#------------ Save Screenshot ------------#
#-----------------------------------------#
# Properties modified on pressureLUT
pressureLUT.UseOpacityControlPointsFreehandDrawing = 1

# get layout
layout1 = GetLayout()

# layout/tab size in pixels
layout1.SetSize(1216, 826)

# current camera placement for renderView1
renderView1.CameraPosition = [-10.315762968342487, -18.656354859694932, 24.221272210988175]
renderView1.CameraFocalPoint = [27.658837270066897, 21.675133751395194, -22.895712798324965]
renderView1.CameraViewUp = [0.5289731493736426, 0.3852885015024361, 0.7561350262034802]
renderView1.CameraParallelScale = 104.65004520189164

# save screenshot
SaveScreenshot('./test1.png', renderView1, ImageResolution=[1216, 826],
    OverrideColorPalette='WhiteBackground')
