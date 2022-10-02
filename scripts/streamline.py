from pvscript import pvScript
from loadpvcc import infopvcc
from utils import is_exist
from paraview.simple import *
from pathlib import Path
import sys

class streamline(pvScript):
    def __init__(self, boundary, field):
        self.boundary = boundary
        self.field    = field
        if not is_exist(self.boundary):
            raise Exception('The file %s doesn\'t exist or is not HDF5 file.'%self.boundary)
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
        self.field.CellArrayStatus = ['Velocity']

    def _filter(self, pos):
        '''
        Create the point data field.
        pos: the position of the slice.
        '''
        #-----------------------------------------#
        #------------ Get A New Slice ------------#
        #-----------------------------------------#
        # create a new 'Slice'
        self.slice = Slice(registrationName='Slice', Input=self.field)
        self.slice.SliceType = 'Plane'
        self.slice.HyperTreeGridSlicer = 'Plane'
        self.slice.SliceOffsetValues = [0.0]
        
        # init the 'Plane' selected for 'SliceType'
        self.slice.SliceType.Origin = [pos, 7.105427357601002e-15, 49.875000000000014]
        
        # Properties modified on slicefield.SliceType
        self.slice.SliceType.Normal = [1.0, 0.0, 0.0]

        #-----------------------------------------#
        #-------- Cell Data To Point Data --------#
        #-----------------------------------------#
        # create a new 'Cell Data to Point Data'
        self.slicepoint = CellDatatoPointData(registrationName='Slicepoint', Input=self.slice)
        self.slicepoint.CellDataArraytoprocess = ['Qcriterion', 'Velocity']
        
        #----------------------------------------#
        #--------- Calculate The Vector ---------#
        #----------------------------------------#
        # create a new 'Calculator'
        self.vel_yz = Calculator(registrationName='Vel_yz', Input=self.slicepoint)
        self.vel_yz.AttributeType = 'Point Data'
        self.vel_yz.ResultArrayName = 'vel_yz'
        self.vel_yz.Function = 'Velocity_VelocityY*jHat+Velocity_VelocityZ*kHat'

        #-----------------------------------------#
        #-------------- Mask Points --------------#
        #-----------------------------------------#
        # create a new 'Mask Points'
        self.vel_yz_mask = MaskPoints(registrationName='Vel_yz_mask', Input=self.vel_yz)
        
        # Properties modified on maskPoints1
        self.vel_yz_mask.OnRatio = 20
        
        # Properties modified on maskPoints1
        self.vel_yz_mask.MaximumNumberofPoints = 50000

        #----------------------------------------#
        #------------- Stream Trace -------------#
        #----------------------------------------#
        # create a new 'Stream Tracer With Custom Source'
        self.vel_yz_stream = StreamTracerWithCustomSource(registrationName='Vel_yz_stream', Input=self.vel_yz,
            SeedSource=self.vel_yz_mask)
        self.vel_yz_stream.Vectors = ['POINTS', 'vel_yz']
        self.vel_yz_stream.MaximumStreamlineLength = 200.0

    def _view(self):
        # Get the render view
        self.renderView1 = GetActiveViewOrCreate('RenderView')
        
        # show data in view
        self.boundDisplay    = Show(self.bound, self.renderView1, 'UnstructuredGridRepresentation')
        
        # show data in view
        self.vel_yz_streamDisplay = Show(self.vel_yz_stream, self.renderView1, 'GeometryRepresentation')

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

        # set scalar coloring
        ColorBy(self.vel_yz_streamDisplay, ('POINTS', 'Vorticity', 'X'))
        
        # get color transfer function/color map for 'Pressure'
        vorticityLUT = GetColorTransferFunction('Vorticity')
        
        # Rescale transfer function
        vorticityLUT.RescaleTransferFunction(-50.0, 50.0)
        
        # get opacity transfer function/opacity map for 'Pressure'
        vorticityPWF = GetOpacityTransferFunction('Vorticity')
        
        # Rescale transfer function
        vorticityPWF.RescaleTransferFunction(-50.0, 50.0)

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

        # save screenshot
        SaveScreenshot(ofile, self.renderView1, ImageResolution=[1216, 826],
            OverrideColorPalette='WhiteBackground')

bound = '/home/xlc/DATA/gt/gt/V13_best_bound.cgns'
field = '/home/xlc/DATA/gt/gt/V13_best.cgns'
plot = streamline(bound, field)
plot._import()
plot._filter(12)
plot._view()
plot._output('stream.png', '/home/xlc/projects/pvplot/pvcc/stream_1.pvcc')
