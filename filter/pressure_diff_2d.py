from pvscript import pvScript
from loadpvcc import infopvcc
from utils import is_exist, list_add
from paraview.simple import *
from pathlib import Path
import sys

class pressurediff(pvScript):
    def __init__(self):
        pass

    def _import(self, field):
        self.field    = field
        if not is_exist(self.field):
            raise Exception('The file %s doesn\'t exist or is not HDF5 file.'%self.field)
        # Read the field
        self.field = CGNSSeriesReader(registrationName='Field',    FileNames=[str(self.field)])
        self.field.Bases = ['Base']
        self.field.CellArrayStatus = ['Pressure', 'Velocity']

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
        self.slice.SliceType.Origin = [100, pos, 49.875000000000014]
        
        # Properties modified on slicefield.SliceType
        self.slice.SliceType.Normal = [0.0, 1.0, 0.0]
