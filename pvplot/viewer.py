from paraview.simple import *
from pvplot.loadpvcc import infopvcc

class layout(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Get the layout
        self.layout = CreateLayout(name='Layout')
        self.layout.SetSize(self.x, self.y)

    def splitLayout(self, hint=0, ratio=0.5, dire='hor'):
        '''
        splitLayout: The function is used to split the layout in ParaView
        -- Input:
            - hint:  The index of the window (hint = 0 as default). 
            - ratio: The split ratio (ratio = 0.5 as default).
            - dire: The direction to split the layout. (vert or hor)
        '''
        if dire == 'vert':
            self.layout.SplitVertical(hint, ratio)
        elif dire == 'hor':
            self.layout.SplitHorizontal(hint, ratio)
        else:
            raise Exception('Please choose the proper direction, vert of hor')

    def assignLayout(self, view, hint):
        '''
        assignLayout is the same as the AssignViewToLayout in paraview.
        '''
        AssignViewToLayout(view=view, layout=self.layout, hint=hint)

    def outputLayout(self, ofile, clevel=5):
        SaveScreenshot(ofile, self.layout, SaveAllViews=1, ImageResolution=[self.x, self.y],
            OverrideColorPalette='WhiteBackground', CompressionLevel=str(clevel))
        
class viewer(object):
    def __init__(self):
        self.renderView = CreateView('RenderView')

    def attachPlot(self, disname, source, ctype, color=None, disconf='GeometryRepresentation', is_axes=False, is_bar=False):
        setattr(self, disname, Show(source , self.renderView, disconf))
        sor = getattr(self, disname)

        # Hide orientation axes
        self.renderView.OrientationAxesVisibility = 0 if not is_axes else 1

        if color is not None:
            if ctype == 'Point':
                # Judge if the color in the Point list
                if color[0] in source.PointData.keys():
                    ColorBy(getattr(self, disname), ('POINTS', *color))
                    setattr(self, disname+'LUT', GetColorTransferFunction(color))
                    setattr(self, disname+'PWF', GetOpacityTransferFunction(color))
                    # show color bar/color legend
                    sor.SetScalarBarVisibility(self.renderView, is_bar)
                else:
                    raise Exception('The data {} is not in the {}.'.format(color[0], source.CellData.keys()))
            if ctype == 'Cell':
                # Judge if the color in the Point list
                if color[0] in source.CellData.keys():
                    ColorBy(getattr(self, disname), ('CELLS', *color))
                    setattr(self, disname+'LUT', GetColorTransferFunction(*color))
                    setattr(self, disname+'PWF', GetOpacityTransferFunction(*color))
                    # show color bar/color legend
                    sor.SetScalarBarVisibility(self.renderView, is_bar)
                else:
                    raise Exception('The data {} is not in the {}.'.format(color[0], source.CellData.keys()))

    def setColorRange(self, disname, lb, rb):
        if hasattr(self, disname):
            LUT = getattr(self, disname+'LUT')
            LUT.RescaleTransferFunction(lb, rb)

    def changeView(self, pvcc):
        ccinfo = infopvcc(pvcc)
        self.renderView.CameraPosition = ccinfo.CameraPosition
        self.renderView.CameraFocalPoint = ccinfo.CameraFocalPoint
        self.renderView.CameraViewUp = ccinfo.CameraViewUp
        self.renderView.CameraParallelScale = ccinfo.CameraParallelScale

    def interactionMode(self, mode):
        self.renderView.InteractionMode = mode

    def outputView(self, ofile, x, y, clevel=5):
        SaveScreenshot(ofile, self.renderView, ImageResolution=[x, y],
            OverrideColorPalette='WhiteBackground', CompressionLevel=str(clevel))
