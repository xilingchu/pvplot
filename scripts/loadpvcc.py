from xml.etree import ElementTree as ET
from pathlib import Path

class infopvcc(object):
    def __init__(self, pvcc):
        pvcc = Path(pvcc).expanduser().resolve()
        self.pvcc = pvcc
        if not pvcc.exists():
            raise Exception('The paraview camera settings is not exists.')
        
        etree = ET.parse(pvcc)
        pvcc   = etree.getroot()
        config = pvcc.find('Proxy')
        for child in config:
            # Get the position 
            if child.attrib['name'] == 'CameraPosition':
                self._position = []
                for gchild in child:
                    self._position.append(float(gchild.attrib['value']))
            # Get the Focus Point 
            if child.attrib['name'] == 'CameraFocalPoint':
                self._focalpoint = []
                for gchild in child:
                    self._focalpoint.append(float(gchild.attrib['value']))
            # Get the Camera View up 
            if child.attrib['name'] == 'CameraViewUp':
                self._cameraviewup = []
                for gchild in child:
                    self._cameraviewup.append(float(gchild.attrib['value']))
            # Get the Camera Parallel Scale
            if child.attrib['name'] == 'CameraParallelScale':
                for gchild in child:
                    self._cameraparallelscale = float(gchild.attrib['value'])

    @property
    def CameraPosition(self):
        return self._position
        
    @property
    def CameraFocalPoint(self):
        return self._focalpoint
    
    @property
    def CameraViewUp(self):
        return self._cameraviewup
        
    @property
    def CameraParallelScale(self):
        return self._cameraparallelscale
                
if __name__ == '__main__':
    a = infopvcc('../pvcc/stream_1.pvcc')
    print(a.CameraPosition, a.CameraParallelScale, a.CameraViewUp, a.CameraFocalPoint)
