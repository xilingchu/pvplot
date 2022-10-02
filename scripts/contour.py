from pvscript import pvScript
from loadpvcc import infopvcc
from utils import is_exist
from paraview.simple import *
from pathlib import Path
import sys

class contour(pvScript):
    '''
    Use paraview to draw contour.
    '''
    def __init__(self, boundary, field):
        self.boundary = boundary
        if not is_exist(self.boundary):
            raise Exception('The file %s doesn\'t exist or is not HDF5 file.'%self.boundary)
        self.field    = field
        if not is_exist(self.field):
            raise Exception('The file %s doesn\'t exist or is not HDF5 file.'%self.field)

    def _import(self):
        # Read the boundary
        self.bound = CGNSSeriesReader(registrationName='Boundary', FileNames=[str(self.boundary)])
        self.bound.Bases = ['Base']
        self.bound.CellArrayStatus = ['SkinFriction']
        # Read the field
        self.field = CGNSSeriesReader(registrationName='Field',    FileNames=[str(self.field)])
        self.field.Bases = ['Base']
        self.field.CellArrayStatus = ['Qcriterion']

    def _filter(self, qnum):
        '''
        Create the point data field.
        qnum: The value of Isosurfaces of Q-criterion.
        '''
        # create a new 'Cell Data to Point Data'
        self.pfield = CellDatatoPointData(registrationName='Pfield', Input=self.field)
        self.pfield.CellDataArraytoprocess = ['Qcriterion']
        # create a new 'Contour'
        self.qcontour = Contour(registrationName='Qcontour', Input=self.pfield)
        self.qcontour.ContourBy = ['POINTS', 'Qcriterion']
        self.qcontour.Isosurfaces = [qnum]
        
    def _view(self):
        # Get the render view
        self.renderView1 = GetActiveViewOrCreate('RenderView')
        
        # show data in view
        self.boundDisplay    = Show(self.bound, self.renderView1, 'UnstructuredGridRepresentation')
         
        self.qcontourDisplay = Show(self.qcontour, self.renderView1, 'GeometryRepresentation')
        
        # Set the scalar color
        ColorBy(self.boundDisplay, ('CELLS', 'SkinFriction', 'SkinFrictionX'))
        
        # show color bar/color legend
        self.boundDisplay.SetScalarBarVisibility(self.renderView1, True)
        
        # get color transfer function/color map for 'Pressure'
        frictionLUT = GetColorTransferFunction('SkinFriction')
        
        # get opacity transfer function/opacity map for 'Pressure'
        frictionPWF = GetOpacityTransferFunction('SkinFriction')

        # Rescale transfer function
        frictionLUT.RescaleTransferFunction(0, 30)
        frictionPWF.RescaleTransferFunction(0, 30)

    def _output(self, ofile, pvcc):
        # get layout
        layout1 = GetLayout()
        
        # layout/tab size in pixels
        layout1.SetSize(1216, 826)

        ccinfo = infopvcc(pvcc)
        self.renderView1.CameraPosition = ccinfo.CameraPosition
        self.renderView1.CameraFocalPoint = ccinfo.CameraFocalPoint
        self.renderView1.CameraViewUp = ccinfo.CameraViewUp
        self.renderView1.CameraParallelScale = ccinfo.CameraParallelScale

        # change interaction mode for render view
        self.renderView1.InteractionMode = '3D'

        # save screenshot
        SaveScreenshot(ofile, self.renderView1, ImageResolution=[1216, 826],
            OverrideColorPalette='WhiteBackground')

bound = '/home/xlc/DATA/gt/gt/V13_best_bound.cgns'
field = '/home/xlc/DATA/gt/gt/V13_best.cgns'
plot = contour(bound, field)
plot._import()
plot._filter(10)
plot._view()
plot._output('test.png', '/home/xlc/projects/pvplot/pvcc/stream_1.pvcc')
